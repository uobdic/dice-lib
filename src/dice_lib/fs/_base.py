from abc import ABC, abstractmethod
from typing import List, Tuple


class FileSystem(ABC):
    def __init__(self, path: str) -> None:
        ...

    @abstractmethod
    def size_of_path(self, path: str) -> Tuple[str, int, float, str]:
        """
        Returns a tuple of (path, size_in_bytes, size_in_largest_unit, largest_unit) for a given path.
        Largest unit is the largest unit where size is smaller than the scale of the next one.
        Scale for sizes is 1024.
        """

    @abstractmethod
    def size_of_paths(self, paths: List[str]) -> List[Tuple[str, int, float, str]]:
        ...

    @abstractmethod
    def get_owner(self, pathstr: str) -> str:
        ...

    @abstractmethod
    def ls(self, path: str) -> List[str]:
        ...

    @abstractmethod
    def mkdir(self, path: str) -> None:
        ...

    @abstractmethod
    def rm(self, path: str) -> None:
        ...

    @abstractmethod
    def rm_recursive(self, path: str) -> None:
        ...

    @abstractmethod
    def copy(self, src: str, dest: str) -> None:
        ...

    @abstractmethod
    def copy_recursive(self, src: str, dest: str) -> None:
        ...

    @abstractmethod
    def move(self, src: str, dest: str) -> None:
        ...
