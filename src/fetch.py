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


class Mark(BaseModel):

    caption: MissingDescription = "Missing"

    subject: str = Field(alias="nazev")

    date: Annotated[str | datetime, MissingDescription, Field(alias="datum")] = "Missing"

    weight: int = Field(ge=1, le=10, alias="vaha")

    mark: MarkValue


def fetch_data(username: str, password: str) -> List[Mark]:
    """
    Fetch data from bakalari website

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
        s.post(LOGIN_URL, data=payload)
        r = s.get(MARKS_URL)

    soup = BeautifulSoup(r.content, "html.parser")
    scripts = soup.find_all("script")

    for script in scripts:
        if "model.items" in script.text:

            if (result := re.search(r"\[\{.*?\}\]", script.text, re.DOTALL)) is None:
                exit() # TODO: logging

            array = json.loads(result.group())

            return [Mark(**mark) for mark in array]
            # print(json.dumps(array, indent=4))

            