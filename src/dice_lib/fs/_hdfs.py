import os
import sys
from typing import Any, List, Optional, Tuple

from plumbum import local
from pyarrow.fs import HadoopFileSystem
import xml.etree.ElementTree as ET

from ..user import current_user
from ..logger import log
from ._base import FileSystem, LsFormat


CONF = "/etc/hadoop/conf/hdfs-site.xml"


def __get_namenodes() -> list[str]:
    """
    Get the list of namenodes from the HDFS configuration file.
    """

    tree = ET.parse(CONF)
    root = tree.getroot()
    namenodes = []

    for prop in root.findall("property"):
        name = prop.find("name")
        if name is None:
            continue
        name_str = str(name.text)

        if name_str.startswith("dfs.namenode.http-address"):
            value = prop.find("value")
            if value is None:
                continue
            namenodes.append(str(value.text))
    return namenodes


def get_hdfs_client(user: str) -> Any:
    """Retrieving the HDFS client to execute operations on HDFS."""
    import pyhdfs

    namenodes = __get_namenodes()
    log.debug("Connecting to HDFS via %s", namenodes)
    client = pyhdfs.HdfsClient(namenodes, user_name=user)  # can throw AssertionError
    return client


class HDFS(FileSystem):
    protocol: str = "hdfs://"

    def __init__(
        self,
        user: Optional[str] = None,
    ):
        self.user = current_user() if user is None else user
        self.fs = get_hdfs_client(self.user)


    def size_of_path(self, path: str) -> Tuple[str, int, float, str]:
        cs = self.fs.content_summary(path)
        total = cs.space_consumed
        total_scaled, unit = convert_to_largest_unit(total, "B", scale=1024)
        return str(path), total, total_scaled, unit

    def size_of_paths(self, paths: List[str]) -> List[Tuple[str, int, float, str]]:
        return [self.size_of_path(path) for path in paths]

    def get_owner(self, pathstr: str) -> str:
        status = self.status(pathstr)
        return status.owner

    def ls(self, path: str) -> LsFormat:
        return self.fs.listdir(path)

    def status(self, path: str) -> dict:
        return self.fs.status(path)

    def mkdir(self, path: str) -> None:
        self.fs.mkdirs(path)

    def rm(self, path: str) -> None:
        log.debug("Removing %s", path)
        self.fs.delete(path)

    def rm_recursive(self, path: str) -> None:
        log.debug("Removing %s", path)
        self.fs.delete(path, recursive=True)

    def copy(self, src: str, dest: str) -> None:
        pass

    def copy_recursive(self, src: str, dest: str) -> None:
        pass

    def move(self, src: str, dest: str) -> None:
        pass
