from pathlib import Path

from pydantic import BaseModel

class PathConfig(BaseModel):
    raw_marks: Path
    results: Path
    log: Path
