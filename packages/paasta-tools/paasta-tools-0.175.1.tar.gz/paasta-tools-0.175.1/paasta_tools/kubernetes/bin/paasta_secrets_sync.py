#!/usr/bin/env python
# Copyright 2015-2019 Yelp Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import argparse
import base64
import hashlib
import json
import logging
import os
import sys
import time
from collections import defaultdict
from functools import partial
from typing import Callable
from typing import Dict
from typing import List
from typing import Optional
from typing import Set

from kubernetes.client.rest import ApiException
from typing_extensions import Literal

from paasta_tools.kubernetes_tools import create_secret
from paasta_tools.kubernetes_tools import create_secret_signature
from paasta_tools.kubernetes_tools import get_paasta_secret_name
from paasta_tools.kubernetes_tools import get_paasta_secret_signature_name
from paasta_tools.kubernetes_tools import get_secret_signature
from paasta_tools.kubernetes_tools import get_vault_key_secret_name
from paasta_tools.kubernetes_tools import KubeClient
from paasta_tools.kubernetes_tools import KubernetesDeploymentConfig
from paasta_tools.kubernetes_tools import sanitise_kubernetes_name
from paasta_tools.kubernetes_tools import update_secret
from paasta_tools.kubernetes_tools import update_secret_signature
from paasta_tools.paasta_service_config_loader import PaastaServiceConfigLoader
from paasta_tools.secret_tools import get_secret_provider
from paasta_tools.utils import DEFAULT_SOA_DIR
from paasta_tools.utils import DEFAULT_VAULT_TOKEN_FILE
from paasta_tools.utils import get_service_instance_list
from paasta_tools.utils import INSTANCE_TYPE_TO_K8S_NAMESPACE
from paasta_tools.utils import INSTANCE_TYPES
from paasta_tools.utils import load_system_paasta_config

log = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Sync paasta secrets into k8s")
    parser.add_argument(
        "service_list",
        nargs="+",
        help="The list of services to sync secrets for",
        metavar="SERVICE",
    )
    parser.add_argument(
        "-c",
        "--cluster",
        dest="cluster",
        metavar="CLUSTER",
        default=None,
        help="Kubernetes cluster name",
    )
    parser.add_argument(
        "-d",
        "--soa-dir",
        dest="soa_dir",
        metavar="SOA_DIR",
        default=DEFAULT_SOA_DIR,
        help="define a different soa config directory",
    )
    parser.add_argument(
        "-n",
        "--namespace",
        dest="namespace",
        help="Overwrite destination namespace for secrets",
    )
    parser.add_argument(
        "-t",
        "--vault-token-file",
        dest="vault_token_file",
        default=DEFAULT_VAULT_TOKEN_FILE,
        help="Define a different vault token file location",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", dest="verbose", default=False
    )
    parser.add_argument(
        "--secret-type",
        choices=["all", "paasta-secret", "boto-key", "crypto-key"],
        default="all",
        type=str,
        help="Define which type of secret to add/update. Default is 'all'",
    )
    args = parser.parse_args()
    return args


def main() -> None:
    args = parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.WARNING)

    system_paasta_config = load_system_paasta_config()
    if args.cluster:
        cluster = args.cluster
    else:
        cluster = system_paasta_config.get_cluster()
    secret_provider_name = system_paasta_config.get_secret_provider_name()
    vault_cluster_config = system_paasta_config.get_vault_cluster_config()
    kube_client = KubeClient()
    services_to_k8s_namespaces = get_services_to_k8s_namespaces(
        service_list=args.service_list,
        cluster=cluster,
        soa_dir=args.soa_dir,
        kube_client=kube_client,
    )

    sys.exit(0) if sync_all_secrets(
        kube_client=kube_client,
        cluster=cluster,
        services_to_k8s_namespaces=services_to_k8s_namespaces,
        secret_provider_name=secret_provider_name,
        vault_cluster_config=vault_cluster_config,
        soa_dir=args.soa_dir,
        vault_token_file=args.vault_token_file,
        overwrite_namespace=args.namespace,
        secret_type=args.secret_type,
    ) else sys.exit(1)


def get_services_to_k8s_namespaces(
    service_list: List[str], cluster: str, soa_dir: str, kube_client: KubeClient
) -> Dict[str, Set[str]]:
    services_to_k8s_namespaces: Dict[str, Set[str]] = defaultdict(set)
    for service in service_list:
        # Special handling for service `_shared`, since it doesn't actually exist
        # Copy shared secrest to all namespaces, assuming that if a secret is declared shared
        # the team is aware that more people can see it
        if service == "_shared":
            services_to_k8s_namespaces[service] = set(
                INSTANCE_TYPE_TO_K8S_NAMESPACE.values()
            )
            paasta_namespaces = kube_client.core.list_namespace(
                label_selector="paasta.yelp.com/managed=true"
            )
            for namespace in paasta_namespaces.items:
                services_to_k8s_namespaces[service].add(namespace.metadata.name)
            continue

        for instance_type in INSTANCE_TYPES:
            if instance_type == "kubernetes":
                config_loader = PaastaServiceConfigLoader(service, soa_dir)
                for service_instance_config in config_loader.instance_configs(
                    cluster=cluster, instance_type_class=KubernetesDeploymentConfig
                ):
                    services_to_k8s_namespaces[service].add(
                        service_instance_config.get_namespace()
                    )
            else:
                instances = get_service_instance_list(
                    service=service,
                    instance_type=instance_type,
                    cluster=cluster,
                    soa_dir=soa_dir,
                )
                if instances:
                    services_to_k8s_namespaces[service].add(
                        INSTANCE_TYPE_TO_K8S_NAMESPACE[instance_type]
                    )

    return dict(services_to_k8s_namespaces)


def sync_all_secrets(
    kube_client: KubeClient,
    cluster: str,
    services_to_k8s_namespaces: Dict[str, Set],
    secret_provider_name: str,
    vault_cluster_config: Dict[str, str],
    soa_dir: str,
    vault_token_file: str,
    secret_type: Literal["all", "paasta-secret", "crypto-key", "boto-key"] = "all",
    overwrite_namespace: Optional[str] = None,
) -> bool:
    results = []

    for service, namespaces in services_to_k8s_namespaces.items():
        sync_service_secrets: Dict[str, List[Callable]] = defaultdict(list)

        if overwrite_namespace:
            namespaces = {overwrite_namespace}
        for namespace in namespaces:
            sync_service_secrets["paasta-secret"].append(
                partial(
                    sync_secrets,
                    kube_client=kube_client,
                    cluster=cluster,
                    service=service,
                    secret_provider_name=secret_provider_name,
                    vault_cluster_config=vault_cluster_config,
                    soa_dir=soa_dir,
                    namespace=namespace,
                    vault_token_file=vault_token_file,
                )
            )
        sync_service_secrets["boto-key"].append(
            partial(
                sync_boto_secrets,
                kube_client=kube_client,
                cluster=cluster,
                service=service,
                soa_dir=soa_dir,
            )
        )
        sync_service_secrets["crypto-key"].append(
            partial(
                sync_crypto_secrets,
                kube_client=kube_client,
                cluster=cluster,
                service=service,
                secret_provider_name=secret_provider_name,
                vault_cluster_config=vault_cluster_config,
                soa_dir=soa_dir,
                vault_token_file=vault_token_file,
            )
        )

        if secret_type == "all":
            results.append(
                all(sync() for sync in sync_service_secrets["paasta-secret"])
            )
            results.append(all(sync() for sync in sync_service_secrets["boto-key"]))
            results.append(all(sync() for sync in sync_service_secrets["crypto-key"]))
        else:
            results.append(all(sync() for sync in sync_service_secrets[secret_type]))

    return all(results)


def sync_secrets(
    kube_client: KubeClient,
    cluster: str,
    service: str,
    secret_provider_name: str,
    vault_cluster_config: Dict[str, str],
    soa_dir: str,
    namespace: str,
    vault_token_file: str,
) -> bool:
    secret_dir = os.path.join(soa_dir, service, "secrets")
    secret_provider_kwargs = {
        "vault_cluster_config": vault_cluster_config,
        # TODO: make vault-tools support k8s auth method so we don't have to
        # mount a token in.
        "vault_auth_method": "token",
        "vault_token_file": vault_token_file,
    }
    secret_provider = get_secret_provider(
        secret_provider_name=secret_provider_name,
        soa_dir=soa_dir,
        service_name=service,
        cluster_names=[cluster],
        secret_provider_kwargs=secret_provider_kwargs,
    )
    if not os.path.isdir(secret_dir):
        log.debug(f"No secrets dir for {service}")
        return True

    with os.scandir(secret_dir) as secret_file_paths:
        for secret_file_path in secret_file_paths:
            if secret_file_path.path.endswith("json"):
                secret = secret_file_path.name.replace(".json", "")
                with open(secret_file_path, "r") as secret_file:
                    secret_signature = secret_provider.get_secret_signature_from_data(
                        json.load(secret_file)
                    )

                if secret_signature:
                    create_or_update_k8s_secret(
                        service=service,
                        signature_name=get_paasta_secret_signature_name(
                            namespace, service, sanitise_kubernetes_name(secret)
                        ),
                        secret_name=get_paasta_secret_name(
                            namespace, service, sanitise_kubernetes_name(secret)
                        ),
                        get_secret_data=(
                            lambda: {
                                secret: base64.b64encode(
                                    # If signatures does not match, it'll sys.exit(1)
                                    secret_provider.decrypt_secret_raw(secret)
                                ).decode("utf-8")
                            }
                        ),
                        secret_signature=secret_signature,
                        kube_client=kube_client,
                        namespace=namespace,
                    )

    return True


def sync_crypto_secrets(
    kube_client: KubeClient,
    cluster: str,
    service: str,
    secret_provider_name: str,
    vault_cluster_config: Dict[str, str],
    soa_dir: str,
    vault_token_file: str,
) -> bool:
    """
    For each key-name in `crypto_key`,
    1. Fetch all versions of the key-name from Vault superregion mapped from cluster, e.g. `kubestage` maps to `devc` Vault server.
    2. Create K8s secret from JSON blob containing all key versions.
    3. Create signatures as K8s configmap based on JSON blob hash.

    So each replica of a service instance gets the same key, thereby reducing requests to Vault API as we only talk to vault during secret syncing
    """
    config_loader = PaastaServiceConfigLoader(service=service, soa_dir=soa_dir)
    for instance_config in config_loader.instance_configs(
        cluster=cluster, instance_type_class=KubernetesDeploymentConfig
    ):
        crypto_keys = instance_config.get_crypto_keys_from_config()
        if not crypto_keys:
            continue
        secret_data = {}
        provider = get_secret_provider(
            secret_provider_name=secret_provider_name,
            soa_dir=soa_dir,
            service_name=service,
            cluster_names=[cluster],
            secret_provider_kwargs={
                "vault_cluster_config": vault_cluster_config,
                "vault_auth_method": "token",
                "vault_token_file": vault_token_file,
            },
        )
        for key in crypto_keys:
            key_versions = provider.get_key_versions(key)
            if not key_versions:
                log.error(
                    f"No key versions found for {key} on {instance_config.get_sanitised_deployment_name()}"
                )
                continue

            secret_data[get_vault_key_secret_name(key)] = base64.b64encode(
                json.dumps(key_versions).encode("utf-8")
            ).decode("utf-8")

        if not secret_data:
            continue

        # In order to prevent slamming the k8s API, add some artificial delay here
        time.sleep(0.3)
        create_or_update_k8s_secret(
            service=service,
            signature_name=instance_config.get_crypto_secret_signature_name(),
            # the secret name here must match the secret name given in the secret volume config,
            # i.e. `kubernetes.client.V1SecretVolumeSource`'s `secret_name` must match below
            secret_name=instance_config.get_crypto_secret_name(),
            get_secret_data=(lambda: secret_data),
            secret_signature=_get_dict_signature(secret_data),
            kube_client=kube_client,
            namespace=instance_config.get_namespace(),
        )

    return True


def sync_boto_secrets(
    kube_client: KubeClient,
    cluster: str,
    service: str,
    soa_dir: str,
) -> bool:
    config_loader = PaastaServiceConfigLoader(service=service, soa_dir=soa_dir)
    for instance_config in config_loader.instance_configs(
        cluster=cluster, instance_type_class=KubernetesDeploymentConfig
    ):
        boto_keys = instance_config.config_dict.get("boto_keys", [])
        if not boto_keys:
            continue
        boto_keys.sort()
        secret_data = {}
        for key in boto_keys:
            for filetype in ["sh", "yaml", "json", "cfg"]:
                this_key = key + "." + filetype
                sanitised_key = this_key.replace(".", "-").replace("_", "--")
                try:
                    with open(f"/etc/boto_cfg_private/{this_key}") as f:
                        secret_data[sanitised_key] = base64.b64encode(
                            f.read().encode("utf-8")
                        ).decode("utf-8")
                except IOError:
                    log.warning(
                        f"Boto key {this_key} required for {service} could not be found."
                    )

        if not secret_data:
            continue

        # In order to prevent slamming the k8s API, add some artificial delay here
        time.sleep(0.3)
        create_or_update_k8s_secret(
            service=service,
            signature_name=instance_config.get_boto_secret_signature_name(),
            secret_name=instance_config.get_boto_secret_name(),
            get_secret_data=(lambda: secret_data),
            secret_signature=_get_dict_signature(secret_data),
            kube_client=kube_client,
            namespace=instance_config.get_namespace(),
        )
    return True


def _get_dict_signature(data: Dict[str, str]) -> str:
    return hashlib.sha1(
        "|".join(f"{key}:{value}" for key, value in data.items()).encode("utf-8")
    ).hexdigest()


def create_or_update_k8s_secret(
    service: str,
    secret_name: str,
    signature_name: str,
    get_secret_data: Callable[[], Dict[str, str]],
    secret_signature: str,
    kube_client: KubeClient,
    namespace: str,
) -> None:
    """
    :param get_secret_data: is a function to postpone fetching data in order to reduce service load, e.g. Vault API
    """
    kubernetes_signature = get_secret_signature(
        kube_client=kube_client,
        signature_name=signature_name,
        namespace=namespace,
    )

    if not kubernetes_signature:
        log.info(f"{secret_name} for {service} in {namespace} not found, creating")
        try:
            create_secret(
                kube_client=kube_client,
                service_name=service,
                secret_name=secret_name,
                secret_data=get_secret_data(),
                namespace=namespace,
            )
        except ApiException as e:
            if e.status == 409:
                log.warning(
                    f"Secret {secret_name} for {service} already exists in {namespace} but no signature found. Updating secret and signature."
                )
                update_secret(
                    kube_client=kube_client,
                    secret_name=secret_name,
                    secret_data=get_secret_data(),
                    service_name=service,
                    namespace=namespace,
                )
            else:
                raise
        create_secret_signature(
            kube_client=kube_client,
            service_name=service,
            signature_name=signature_name,
            secret_signature=secret_signature,
            namespace=namespace,
        )
    elif secret_signature != kubernetes_signature:
        log.info(
            f"{secret_name} for {service} in {namespace} needs updating as signature changed"
        )
        update_secret(
            kube_client=kube_client,
            secret_name=secret_name,
            secret_data=get_secret_data(),
            service_name=service,
            namespace=namespace,
        )
        update_secret_signature(
            kube_client=kube_client,
            service_name=service,
            signature_name=signature_name,
            secret_signature=secret_signature,
            namespace=namespace,
        )
    else:
        log.info(f"{secret_name} for {service} in {namespace} up to date")


if __name__ == "__main__":
    main()
