import tomllib
import logging
import os

from pydantic import BaseModel

logger = logging.getLogger(__name__)

try:
    with open("config.toml", "rb") as f:
        config = tomllib.load(f)
    logger.debug("Loading configuration succesfull")

except:
    logger.critical("Loading configuration failed")
    exit()

try:
    LOGIN_URL = config["server"]["base_url"] + config["server"]["login_endpoint"]
    MARKS_URL = config["server"]["base_url"] + config["server"]["marks_endpoint"]
    JSON_MARKS = config["path"]["json_marks"]
    RESULT_MARKS = config["path"]["results"]

    logger.debug("Assigning confif constants succesfull")

except:
    logger.critical("Assigning config constants failed")
    exit()

