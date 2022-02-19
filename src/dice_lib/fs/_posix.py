from pathlib import Path
from typing import List, Tuple

from plumbum import local
from plumbum.commands.base import BoundCommand

from dice_lib.units import convert_to_largest_unit

from ._base import FileSystem


class PosixFileSystem(FileSystem):
    def __init__(self, path: str) -> None:
        self._path: Path = Path(path)
        self._size_cmd: BoundCommand = local["nice"]["-n19", "du"]["-s"]

    def get_owner(self, pathstr: str) -> str:
        path = Path(pathstr)
        return path.owner()

    def size_of_path(self, path: str) -> Tuple[str, int, float, str]:
        total, _ = self._size_cmd(path).split()
        total = int(total)
        total_scaled, unit = convert_to_largest_unit(total, "B", scale=1024)
        return str(path), total, total_scaled, unit

    def __size_of_path(
        self, path: str, size_cmd: BoundCommand
    ) -> Tuple[str, int, float, str]:
        tmp = self._size_cmd
        self._size_cmd = size_cmd
        result = self.size_of_path(path)
        self._size_cmd = tmp
        return result

    def size_of_paths(self, paths: List[str]) -> List[Tuple[str, int, float, str]]:
        return [
            self.__size_of_path(path, lambda path: self._size_cmd[path]())
            for path in paths
        ]
