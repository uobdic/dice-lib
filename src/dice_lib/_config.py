from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any

from omegaconf import OmegaConf

DEFAULT_DICE_CONFIG_PATH = "/etc/dice/config.yaml"


class ServerStatus(Enum):
    ONLINE = "online"
    OFFLINE = "offline"
    ACTIVE = "active"
    RETIRED = "retired"
    COMMISSIONING = "commissioning"
    DECOMMISSIONING = "decommissioning"


@dataclass
class ComputingElement:
    name: str
    status: str
    type: str


@dataclass
class StorageElement:
    name: str
    status: str
    type: str
    endpoints: dict[str, str]
    root_dir: str


@dataclass
class ComputingGrid:
    site_name: str
    cms_site_name: str
    computing_elements: list[ComputingElement]
    storage_elements: list[StorageElement]
    FTS_SERVERS: list[str]


@dataclass
class Storage:
    mounts: list[str]
    binaries: dict[str, str] | None
    env: dict[str, str] | None
    extras: dict[str, Any] | None
    protocol: str | None = "file://"
    remove_mount_for_native_access: bool | None = False


@dataclass
class LoginNode:
    name: str
    status: ServerStatus
    group: str


@dataclass
class DiceConfig:
    cluster_name: str
    documentation: str
    login_nodes: list[LoginNode]
    computing_grid: ComputingGrid
    storage: dict[str, Storage]
    glossary: dict[str, str]
    site_info: dict[str, Any]
    node_info: dict[str, Any]


def load_config(config_file: str = DEFAULT_DICE_CONFIG_PATH) -> Any:
    path = Path(config_file)
    if not path.exists():
        msg = f"DICE config, {config_file}, does not exist. Please contact dice-admin"
        raise FileNotFoundError(msg)
    schema = OmegaConf.structured(DiceConfig)
    conf = OmegaConf.load(path)
    return OmegaConf.merge(schema, conf)
