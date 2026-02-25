from load_config import LOGIN_URL, MARKS_URL
import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel, Field, BeforeValidator
from typing import Annotated, Literal, List
import re
import json
from datetime import datetime


# === HELP FUNCS TO VALIDATIONS === #
def clean_mark(m: str) -> str | int:
    """
    Convert str to int & from '1-' (which is not number) make '-1'

    Args:
        m (str): mark to check
    Returns:
        int | str: correct mark
    """

    m = m.strip()

    if len(m) > 1:
        return int(m[::-1])
    if m.isnumeric():
        return int(m)
    
    return m

# === OWN ANNOTATED === #
MissingDescription = Annotated[
    str,
    BeforeValidator(lambda x: x),  # TODO: loggging
    Field(default="Missing")
]

MarkValue = Annotated[
    int | Literal["N", "X"],
    BeforeValidator(clean_mark),
    Field(alias="MarkText")
]


# === MARK MODEL === #
class Mark(BaseModel):
    """
    Represent one mark fetched from bakalari website
    """

    caption: Annotated[MissingDescription, Field(description="description of mark")] = "Missing"

    subject: str = Field(alias="nazev", description="name of the subject")

    date: Annotated[str | datetime, MissingDescription, Field(alias="datum", description="date when mark was added to baka system")] = "Missing"

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
            exit() # TODO: logging

        r = s.get(MARKS_URL)
        if r.status_code != 200:
            exit() # TODO: logging


    # === FIND EXCACTLY THAT ONE SCRIPT FROM ENTIRE HTML SOURCE CODE === #
    soup = BeautifulSoup(r.content, "html.parser")
    scripts = soup.find_all("script")

    for script in scripts:
        if "model.items" in script.text:

            if (result := re.search(r"\[\{.*?\}\]", script.text, re.DOTALL)) is None:
                exit() # TODO: logging

            array = json.loads(result.group())
            # print(json.dumps(array, indent=4))

            return [Mark(**mark) for mark in array]
    else:
        exit() # TODO: logging