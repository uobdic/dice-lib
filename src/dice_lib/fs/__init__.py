from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

from .._config import DEFAULT_DICE_CONFIG_PATH, load_config
from ._base import FileSystem
from ._davix import DavixFileSystem
from ._gridftp import GridFTPFileSystem
from ._hdfs import HDFS
from ._posix import PosixFileSystem
from ._s3 import S3FileSystem

FACTORIES: dict[str, type[FileSystem]] = {
    # "davs://": DavixFileSystem,
    "hdfs://": HDFS,
    # "gsiftp://": GridFTPFileSystem,
    "file://": PosixFileSystem,
    # "s3://": S3FileSystem,
    # "root://": XrootDFileSystem,
    "Default": PosixFileSystem,
}

MountSettings = Dict[str, Any]

__all__ = [
    "FileSystem",
    "DavixFileSystem",
    "HDFS",
    "GridFTPFileSystem",
    "PosixFileSystem",
    "S3FileSystem",
    "XRootDFileSystem",
]


def _deduce_fs_from_path(path: str | Path) -> FileSystem:
    for prefix, factory in FACTORIES.items():
        if str(path).startswith(prefix):
            return factory()
    return FACTORIES["Default"]()


def get_mount_settings_from_config(config: dict[str, Any]) -> MountSettings:
    mount_settings = {}
    storage = config.get("storage", {})
    for settings in storage.values():
        protocol = settings.get("protocol", "file://")
        mounts = settings.get("mounts", [])
        remove_mount_for_native_access = settings.get(
            "remove_mount_for_native_access", False
        )
        mount_settings.update(
            {
                mount: {
                    "protocol": protocol,
                    "remove_mount_for_native_access": remove_mount_for_native_access,
                }
                for mount in mounts
            }
        )
    return mount_settings


def prepare_paths(paths: list[str], mount_settings: MountSettings) -> list[str]:
    """
    1. Remove trailing slashes from paths
    2. lookup file system mounts
    3. Replace protocols (e.g. /hdfs/<path> --> hdfs://<path>)
    4. If no protocol is specified, assume local filesystem
    """
    processed_paths = [path.rstrip("/") for path in paths]
    for mount, settings in mount_settings.items():
        for path in processed_paths:
            processed_path = path
            if path.startswith(mount):
                protocol = settings.get("protocol", "file://")
                remove_mount_for_native_access = settings.get(
                    "remove_mount_for_native_access", False
                )
                if remove_mount_for_native_access:
                    processed_path = path[len(mount) :]
                processed_paths[processed_paths.index(path)] = protocol + processed_path
    return processed_paths


class FSClient:
    def __init__(self, config_path: str = DEFAULT_DICE_CONFIG_PATH):
        config = load_config(config_path)
        self.mount_settings = get_mount_settings_from_config(config)

    def get_owner(self, pathstr: str) -> str:
        pathstr = prepare_paths([pathstr], self.mount_settings)[0]
        fs = _deduce_fs_from_path(pathstr)
        return fs.get_owner(pathstr)

    def size_of_paths(self, paths: list[str]) -> list[tuple[str, int, float, str]]:
        paths = prepare_paths(paths, self.mount_settings)
        fs = _deduce_fs_from_path(paths[0])
        return fs.size_of_paths(paths)
