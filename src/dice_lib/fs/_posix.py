from pathlib import Path

from ._base import FileSystem


class PosixFileSystem(FileSystem):


    def get_owner(pathstr: str) -> str:
        path = Path(pathstr)
        return path.owner()
