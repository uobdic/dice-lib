from typing import Tuple

def convert_to_largest_unit(
    value: float, unit: str, scale: float = 1000.0
) -> Tuple[float, str]:
    """Converts value to largest unit of the same type"""
    prefixes = ["", "k", "M", "G", "T", "P", "E", "Z", "Y"]
    current_scale = value
    prefix_index = 0
    for i, _ in enumerate(prefixes):
        if current_scale < scale:
            prefix_index = i
            break
        current_scale /= scale
    return current_scale, prefixes[prefix_index] + unit
