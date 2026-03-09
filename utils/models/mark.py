import logging
from typing import Annotated
from datetime import datetime

from pydantic import Field, BeforeValidator, BaseModel, model_validator, field_validator

logger = logging.getLogger(__name__)

class Mark(BaseModel):
    """Represent one mark fetched from Bakalari website"""
    caption: str = None
    subject: str = Field(alias="nazev")
    date: datetime = Field(alias="datum", default=None)
    weight: int = Field(ge=1, le=10, alias="vaha")
    mark: float = Field(alias="MarkText")
    id_: str = Field(alias="id", default=None)

    @model_validator(mode="after")
    def _check_missing(self) -> "Mark":
        """Raise WARNING log if some values are missing"""
        missing_list = [attr for attr in list(self.model_fields.keys()) if not getattr(self, attr) and attr != self.id_]
        if missing_list:
            missing_values = ", ".join(missing_list)
            logger.warning(f"Mark '{self.id_}' missing values: {missing_values}")
        return self

    @field_validator("mark", mode="before")
    @classmethod
    def _parse_mark(cls, v) -> float:
        v = v.strip()

        if len(v) > 1 and v[1] == "-":
            return float(v[0]) + 0.5
        elif v.isnumeric():
            return float(v)
        else:
            return -1
