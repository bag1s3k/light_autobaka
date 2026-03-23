import tomllib
import logging
from typing import Any
import json

from config.models.app_config import AppConfig
from utils.constants import IS_GITHUB_ACTIONS
from utils.models.progress_config import update_progress

logger = logging.getLogger(__name__)

@update_progress("Loading config")
def _load_config(path: str = None) -> dict[str, Any]:
    """
    Load config from config file

    Returns:
        dict: return dictionary with configuration, otherwise program ends
    """
    from utils.constants import CONFIG_PATH

    if not path:
        path = CONFIG_PATH
    try:
        with open(path, "rb") as f:
            config = tomllib.load(f)
        logger.debug("Loading configuration successful")
        return config
    except:
        logger.exception("Something went wrong while loading configuration")
        raise

def _load_config_env() -> dict[str, Any]:
    """Load config from env variable (CI environment)"""
    from utils.models.env_vars import env_variables

    return json.loads(env_variables.school_data)

if not IS_GITHUB_ACTIONS:
    appconfig = AppConfig(**_load_config())
else:
    appconfig = AppConfig(**{"server": _load_config_env()})
