import json
import os
import tomllib
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel, HttpUrl, computed_field, TypeAdapter, Field


PROJECT_ROOT = Path(__file__).resolve().parents[2]
IS_GITHUB_ACTIONS = os.getenv("GITHUB_ACTIONS") == "true"
DEFAULT_PATH_CONFIG = {
    "raw_marks": PROJECT_ROOT / "output/marks.json",
    "results": PROJECT_ROOT / "output/results.txt",
    "log": PROJECT_ROOT / "output/logs.log",
    "html_template": Path(__file__).with_name("template_index.html"),
    "html_output": PROJECT_ROOT / "index.html",
}


class ServerConfig(BaseModel):
    base_url: HttpUrl
    login_endpoint: str = Field(alias="login_endpoint")
    marks_endpoint: str = Field(alias="marks_endpoint")
    after_login_endpoint: str = Field(alias="after_login_endpoint")

    @computed_field
    def login_url(self) -> HttpUrl:
        """Returns full login url"""
        return self._combine_url(self.login_endpoint)

    @computed_field
    def marks_url(self) -> HttpUrl:
        """Returns full marks url"""
        return self._combine_url(self.marks_endpoint)

    @computed_field
    def success_url(self) -> HttpUrl:
        """Returns url which is immediately display after you login. It's used for successful verification"""
        return self._combine_url(self.after_login_endpoint)

    def _combine_url(self, endpoint: str) -> HttpUrl:
        """Returns combine base url (base url + endpoint)"""
        return TypeAdapter(HttpUrl).validate_python(f"{self.base_url}{endpoint}")


class PathConfig(BaseModel):
    raw_marks: Path
    results: Path
    log: Path
    html_template: Path
    html_output: Path


class AppConfig(BaseModel):
    server: ServerConfig
    path: PathConfig = PathConfig(**DEFAULT_PATH_CONFIG)


class Credentials(BaseModel):
    username: str
    password: str


def load_credentials() -> Credentials:
    load_dotenv()
    username = os.getenv("BAKA_USERNAME")
    password = os.getenv("BAKA_PASSWORD")
    if username is None:
        raise ValueError("Failed to load BAKA_USERNAME")
    if password is None:
        raise ValueError("Failed to load BAKA_PASSWORD")
    return Credentials(username=username, password=password)


def load_config() -> AppConfig:
    if IS_GITHUB_ACTIONS:
        raw = os.getenv("SCHOOL_DATA")
        if raw is None:
            raise ValueError("Failed to load SCHOOL_DATA")
        return AppConfig(server=ServerConfig.model_validate(json.loads(raw)))

    config_path = PROJECT_ROOT / "config.toml"
    if not config_path.is_file():
        raise FileNotFoundError(f"There is no config file at {config_path}")
    with config_path.open("rb") as file:
        data = tomllib.load(file)
    if "path" in data:
        paths = {**DEFAULT_PATH_CONFIG, **data["path"]}
        for key, value in paths.items():
            path = Path(value)
            if not path.is_absolute():
                paths[key] = PROJECT_ROOT / path
        data["path"] = paths
    return AppConfig.model_validate(data)
