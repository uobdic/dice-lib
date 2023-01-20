from typing import Any, Dict, List, Tuple, Type

from ._base import FileSystem
from ._davix import DavixFileSystem
from ._gridftp import GridFTPFileSystem
from ._hdfs import HDFS
from ._posix import PosixFileSystem
from ._s3 import S3FileSystem
from ._xrootd import XrootDFileSystem

FACTORIES: Dict[str, Type[FileSystem]] = {
    "davs://": DavixFileSystem,
    "hdfs://": HDFS,
    "gsiftp://": GridFTPFileSystem,
    "file://": PosixFileSystem,
    "s3://": S3FileSystem,
    "root://": XrootDFileSystem,
    "Default": PosixFileSystem,
}

__all__ = [
    "FileSystem",
    "DavixFileSystem",
    "HDFS",
    "GridFTPFileSystem",
    "PosixFileSystem",
    "S3FileSystem",
    "XRootDFileSystem",
]


def __deduce_fs_from_path(path: str) -> FileSystem:
    for prefix, factory in FACTORIES.items():
        if path.startswith(prefix):
            return factory(path)
    return FACTORIES["Default"](path)


def get_owner(pathstr: str) -> str:
    fs = __deduce_fs_from_path(pathstr)
    return fs.get_owner(pathstr)


def size_of_paths(paths: List[str]) -> List[Tuple[str, int, float, str]]:
    fs = __deduce_fs_from_path(paths[0])
    return fs.size_of_paths(paths)


def get_mount_settings_from_config(config: Dict[str, Any]) -> Dict[str, Any]:
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


def prepare_paths(paths: List[str], mount_settings: Dict[str, Any]) -> List[str]:
    """
    1. Remove trailing slashes from paths
    2. lookup file system mounts
    3. Replace protocols (e.g. /hdfs/<path> --> hdfs://<path>)
    4. If no protocol is specified, assume local filesystem
    """
    processed_paths = [path.rstrip("/") for path in paths]
    for mount, settings in mount_settings.items():
        for path in processed_paths:
            original_path = path
            if path.startswith(mount):
                protocol = settings.get("protocol", "file://")
                remove_mount_for_native_access = settings.get(
                    "remove_mount_for_native_access", False
                )
                if remove_mount_for_native_access:
                    path = path[len(mount) :]
                processed_paths[processed_paths.index(original_path)] = protocol + path
    return processed_paths
