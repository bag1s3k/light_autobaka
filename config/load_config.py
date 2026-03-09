import tomllib
import logging
from typing import Any

from config.models import AppConfig
from utils.constants import CONFIG_PATH

logger = logging.getLogger(__name__)

def _load_config(path: str = CONFIG_PATH) -> dict[str, Any]:
    """
    Load config from config file

    Returns:
        dict: return dictionary with configuration, otherwise program ends
    """
    try:
        with open(path, "rb") as f:
            config = tomllib.load(f)
        logger.debug("Loading configuration successful")
        return config
    except:
        logger.exception("Something went wrong while loading configuration")
        raise

appconfig = AppConfig(**_load_config())
