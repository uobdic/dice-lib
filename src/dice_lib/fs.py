from pathlib import Path
from typing import List, Tuple

from plumbum import local
from plumbum.commands.base import BoundCommand

from .units import convert_to_largest_unit


def size_of_path(path: Path, size_cmd: BoundCommand) -> Tuple[str, int, float, str]:
    """
    Returns a tuple of (path, size_in_bytes, size_in_largest_unit, largest_unit) for a given path.
    Largest unit is the largest unit where size is smaller than the scale of the next one.
    Scale for sizes is 1024.
    """
    total, _ = size_cmd(path).split()
    total = int(total)
    total_scaled, unit = convert_to_largest_unit(total, "B", scale=1024)
    return str(path), total, total_scaled, unit


def size_of_paths(paths: List[Path]) -> List[Tuple[str, int, float, str]]:
    du = local["du"]
    return [size_of_path(path, lambda path: du["-s", path]()) for path in paths]


def get_owner(path: str) -> str:
    """
    Returns the owner of the path.
    """
    return Path(path).owner()
