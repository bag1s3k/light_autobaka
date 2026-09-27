import logging
from datetime import datetime

from pydantic import BaseModel, Field, field_validator


logger = logging.getLogger(__name__)


class BakaError(Exception):
    pass


class LoginError(BakaError):
    pass


class FetchError(BakaError):
    pass


class DataExtractionError(BakaError):
    pass


class Mark(BaseModel):
    """One mark returned by Bakaláři."""

    caption: str | None = None
    subject: str = Field(alias="nazev")
    date: datetime | None = Field(default=None, alias="datum")
    weight: int = Field(ge=1, le=10, alias="vaha")
    mark: float = Field(alias="MarkText")
    id_: str | None = Field(default=None, alias="id")

    @field_validator("mark", mode="before")
    @classmethod
    def parse_mark(cls, value: str) -> float:
        value = value.strip()
        if len(value) > 1 and value[1] == "-":
            return float(value[0]) + 0.5
        if value.isnumeric():
            return float(value)
        return -1.0
