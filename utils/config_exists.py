import os
import logging

from utils.constants import CONFIG_PATH

logger = logging.getLogger(__name__)

def config_exists(path: str = CONFIG_PATH) -> None:
    """Check if config file exists"""
    if not os.path.exists(path):
        logger.critical(f"There is not config file, config file should be in {path}")
        return
