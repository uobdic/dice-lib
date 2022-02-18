from typing import Dict, Type

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
