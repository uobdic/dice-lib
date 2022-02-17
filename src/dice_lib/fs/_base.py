from abc import ABC, abstractmethod
from typing import List, Tuple


class FileSystem(ABC):

    @abstractmethod
    def size_of_path(path: str) -> Tuple[str, int, float, str]:
        ...

    @abstractmethod
    def size_of_paths(paths: List[str]) -> List[Tuple[str, int, float, str]]:
        ...

    @abstractmethod
    def get_owner(pathstr: str) -> str:
        ...

    @abstractmethod
    def ls(self, path: str) -> list:
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
