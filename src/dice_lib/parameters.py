from pathlib import Path
from typing import Any

from omegaconf import OmegaConf

from ._config import DiceConfig

DEFAULT_DICE_CONFIG_PATH = "/etc/dice/config.yaml"


def load_parameters(parameters_file: str = DEFAULT_DICE_CONFIG_PATH) -> Any:
    path = Path(parameters_file)
    if not path.exists():
        raise FileNotFoundError(
            f"DICE config, {parameters_file}, does not exist. Please contact dice-admin"
        )
    schema = OmegaConf.structured(DiceConfig)
    conf = OmegaConf.load(path)
    merged_conf = OmegaConf.merge(schema, conf)
    return merged_conf
