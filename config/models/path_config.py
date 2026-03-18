from pathlib import Path

from pydantic import BaseModel, field_validator

from utils import PROJECT_ROOT

class PathConfig(BaseModel):
    raw_marks: Path
    results: Path
    log: Path
    html_template: Path
    html_output: Path

    @field_validator("raw_marks", "results", "log", "html_template", "html_output", mode="before")
    @classmethod
    def make_path_absolut(cls, v: str) -> str:
        if v.startswith("./"):
            return str(PROJECT_ROOT / v.lstrip("./"))
        return v