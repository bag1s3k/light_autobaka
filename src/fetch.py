import logging
import re
import json

import requests
from bs4 import BeautifulSoup

from load_config import LOGIN_URL, MARKS_URL
from export import export_json
from utils import Mark

logger = logging.getLogger(__name__)


# === FETCH DATA === #
def fetch_data(username: str, password: str) -> list["Mark"]:
    """
    Fetch data from bakalari website
    You receive entire html source code and there's one script where u can find
    everything what you need. Than javascript is converted to json style

    Args:
        username (str)
        password (str)
    Returns:
        List[Mark]: List of parsed marks
    """
    payload = {
        "username": username,
        "password": password
    }

    with requests.session() as s:
        if s.post(LOGIN_URL, data=payload).status_code != 200:
            logger.critical("Login failed")
            exit()

        r = s.get(MARKS_URL)
        if r.status_code != 200:
            logger.critical("Error with interacting on mark's page")
            exit()



    # === FIND EXCACTLY THAT ONE SCRIPT FROM ENTIRE HTML SOURCE CODE === #
    soup = BeautifulSoup(r.content, "html.parser")

    regex_script = re.compile(r"model\.items\s*=\s*")
    raw_script = soup.find("script", string=regex_script) # pyright: ignore[reportArgumentType, reportCallIssue]
    if raw_script is None:
        logger.error("Marks not found")

    raw_data = re.search(r"\[\{.*?\}\]", raw_script.text, re.DOTALL)
    if raw_data is None:
        logger.error("Marks not found")

    data = json.loads(raw_data.group()) # pyright: ignore[reportOptionalMemberAccess]
    # print(json.dumps(data, indent=4))

    logger.info("Data fetched sucessfully")
    export_json(data)
    
    return [Mark(**raw_mark) for raw_mark in data]
    # return [Mark(**raw_mark) for raw_mark in []]