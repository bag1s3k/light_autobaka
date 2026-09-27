import json
import logging
import re
from typing import Any

import requests
from bs4 import BeautifulSoup

from .config import AppConfig, Credentials
from .models import DataExtractionError, FetchError, LoginError, Mark


logger = logging.getLogger(__name__)


def extract_data(soup: BeautifulSoup) -> list[dict[str, Any]]:
    """Read the JSON array assigned to model.items in the marks page."""
    script_pattern = re.compile(r"model\.items\s*=\s*\[\{.*?}]", re.DOTALL)
    script = soup.find("script", string=script_pattern)
    if script is None or script.string is None:
        raise DataExtractionError("Script which contains data not found")

    match = re.search(r"\[\{.*?}]", script.string, re.DOTALL)
    if match is None:
        raise DataExtractionError("Script doesn't contain what we expect")
    return json.loads(match.group())


def fetch_data(config: AppConfig, credentials: Credentials) -> tuple[list[Mark], list[dict[str, Any]]]:
    """Log in, fetch the marks page, and return parsed and raw marks."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Connection": "keep-alive",
    }
    with requests.Session() as session:
        login_response = session.post(
            str(config.server.login_url),
            data={"username": credentials.username, "password": credentials.password},
            headers=headers,
        )
        if login_response.status_code != 200 or login_response.url != str(config.server.success_url):
            raise LoginError("Login failed")

        target_response = session.get(str(config.server.marks_url))
        if target_response.status_code != 200:
            raise FetchError("Fetching data failed")

    raw_marks = extract_data(BeautifulSoup(target_response.content, "lxml"))
    marks = [Mark.model_validate(raw_mark) for raw_mark in raw_marks]
    logger.info("Marks fetched and parsed successfully")
    return marks, raw_marks
