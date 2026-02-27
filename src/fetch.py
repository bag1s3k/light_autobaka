from load_config import LOGIN_URL, MARKS_URL
from utils import MissingDescription, MarkValue
import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel, Field
from typing import Annotated, List
import re
import json
from datetime import datetime
import logging
from export import export_json

logger = logging.getLogger(__name__)


# === MARK MODEL === #
class Mark(BaseModel):
    """
    Represent one mark fetched from bakalari website
    """

    caption: Annotated[MissingDescription, Field(description="description of mark")] = None

    subject: str = Field(alias="nazev", description="name of the subject")

    date: Annotated[str | None | datetime, MissingDescription, Field(alias="datum", description="date when mark was added to baka system")] = None

    weight: int = Field(ge=1, le=10, alias="vaha", description="Weight of the mark")

    mark: MarkValue


# === FETCH DATA === #
def fetch_data(username: str, password: str) -> List[Mark]:
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

    raw_script = soup.find("script", string=re.compile(r"model\.items\s*=\s*")) # pyright: ignore[reportArgumentType, reportCallIssue]
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