from load_config import LOGIN_URL, MARKS_URL
import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel, Field, BeforeValidator
from typing import Annotated, List
import re
import json
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

# === HELP FUNCS TO VALIDATIONS === #
def clean_mark(m: str) -> float:
    """
    Convert str to int & from '1-' (which is not number) make '-1'

    Args:
        m (str): mark to check
    Returns:
        int | str: correct mark
    """

    m = m.strip()

    if len(m) > 1:
        return float(m[0]) + 0.5
    
    if m.isnumeric():
        return float(m)
    else:
        return 0.0

def is_empty(s) -> str:
    """Tell me if there is missing value"""
    
    if s is None:
        logger.warning("Field is empty")
    
    return s

# === OWN ANNOTATED === #
MissingDescription = Annotated[
    str | None,
    BeforeValidator(is_empty),
    Field(default="Missing")
]

MarkValue = Annotated[
    float,
    BeforeValidator(clean_mark),
    Field(alias="MarkText")
]


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
            logger.error("Error with interacting on mark's page")
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

    return [Mark(**raw_mark) for raw_mark in data]