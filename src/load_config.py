import tomllib
import logging

logger = logging.getLogger(__name__)

with open("config.toml", "rb") as f:
    config = tomllib.load(f)

LOGIN_URL = config["server"]["base_url"] + config["server"]["login_endpoint"]
MARKS_URL = config["server"]["base_url"] + config["server"]["marks_endpoint"]
JSON_MARKS = config["path"]["json_marks"]
RESULT_MARKS = config["path"]["results"]

logger.debug("Loading config with no error")