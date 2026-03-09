import logging
import re
import json
from typing import Any

import requests
from bs4 import BeautifulSoup

from config import appconfig
from utils import Mark, Export
from core.exceptions import LoginError, FetchError, DataExtractionError

logger = logging.getLogger(__name__)

def _extract_data(soup: BeautifulSoup) -> Any:
    regex_script = re.compile(r"model\.items\s*=\s*\[\{.*?}]")
    raw_script = soup.find("script", text=regex_script)

    if raw_script is None:
        error_script_not_found = "Script which contains data not found"
        logger.error(error_script_not_found)
        raise DataExtractionError(error_script_not_found)

    if (raw_data := re.search(r"\[\{.*?}]", raw_script.text, re.DOTALL)) is None:
        error_something_different = "Script doesn't contain what we expect"
        logger.error(error_something_different)
        raise DataExtractionError(error_something_different)

    if not (match := raw_data.group()):
        logger.warning("It seems that there aren't any marks")

    logger.info("Data successfully extracted")
    return json.loads(match)

def fetch_data(username: str, password: str) -> list["Mark"]:
    """
    Fetch data from Bakalari website
    You receive entire HTML source code and there's one script where u can find
    everything what you need. Than JavaScript is converted to JSON style

    Returns:
        List[Mark]: List of parsed marks
    """
    payload = {
        "username": username,
        "password": password
    }

    with requests.session() as s:
        if s.post(str(appconfig.server.login_url), data=payload).status_code != 200:
            error_login_failed = "Login failed"
            logging.critical(error_login_failed)
            raise LoginError(error_login_failed)

        r = s.get(str(appconfig.server.marks_url))
        if r.status_code != 200:
            error_fetch_data = "Fetching data fails"
            logging.critical(error_fetch_data)
            raise FetchError(error_fetch_data)

    soup = BeautifulSoup(r.content, "lxml")
    logger.info("Data fetched successfully")

    data = _extract_data(soup)
    Export(data).fetched_data()
    
    return [Mark(**raw_mark) for raw_mark in data]
