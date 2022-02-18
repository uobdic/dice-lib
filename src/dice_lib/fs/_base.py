from abc import ABC, abstractmethod
from typing import List, Tuple


class FileSystem(ABC):
    def __init__(self, path: str) -> None:
        ...

    @abstractmethod
    def size_of_path(self, path: str) -> Tuple[str, int, float, str]:
        ...

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
