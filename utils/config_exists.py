import os
import logging

from utils.constants import CONFIG_PATH
from core.exceptions import ConfigFileError
from utils.models.progress_config import update_progress

logger = logging.getLogger(__name__)

@update_progress("Checking configuration")
def config_exists(path: str = CONFIG_PATH) -> None:
    """Check if config file exists"""
    if not os.path.exists(path):
        raise ConfigFileError(f"There is not config file, config file should be in {path}")

    logger.debug(f"Config file was found on path: {path}")