import logging
import re
import json
from typing import Any

import requests
from bs4 import BeautifulSoup

from config import appconfig
from utils import Mark, Export, login_details
from core.exceptions import LoginError, FetchError, DataExtractionError

logger = logging.getLogger(__name__)

def _extract_data(soup: BeautifulSoup) -> Any:
    """Extracts mark data from a JSON object embedded in a script tag within the Bakalari HTML source."""
    regex_script = re.compile(r"model\.items\s*=\s*\[\{.*?}]")
    raw_script = soup.find("script", text=regex_script)

    if raw_script is None:
        logger.error("Script which contains data not found")
        raise DataExtractionError("Script which contains data not found")

    if (mark_data := re.search(r"\[\{.*?}]", raw_script.text, re.DOTALL)) is None:
        logger.error("Script doesn't contain what we expect")
        raise DataExtractionError("Script doesn't contain what we expect")

    if not (match := mark_data.group()):
        logger.warning("It seems that there aren't any marks")

    logger.info("Data successfully extracted")
    return json.loads(match)

def fetch_data() -> list["Mark"]:
    """
    Fetch HTML code to extract it

    Returns:
        List[Mark]: List of parsed marks
    """
    payload = {
        "username": login_details.username,
        "password": login_details.password
    }

    user_agent = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Connection": "keep-alive",
    }

    # I'm wanna hold session, cause of future use (I wanna implement async scraping
    # of multiple pages, not only marks, but also e.g. timetable, ...)
    # Otherwise I would use 'request.get("...", auth=("", ""))'
    with requests.session() as s:
        login_response = s.post(str(appconfig.server.login_url), data=payload, headers=user_agent)
        if login_response.status_code != 200 or login_response.url != str(appconfig.server.success_url):
            logging.critical("Login failed")
            raise LoginError("Login failed")

        target_response = s.get(str(appconfig.server.marks_url))
        if target_response.status_code != 200:
            logging.critical("Fetching data fails")
            raise FetchError("Fetching data fails")

    soup = BeautifulSoup(target_response.content, "lxml")
    logger.info("Data fetched successfully")

    data = _extract_data(soup)
    Export(data).fetched_data()
    
    return [Mark(**raw_mark) for raw_mark in data]
