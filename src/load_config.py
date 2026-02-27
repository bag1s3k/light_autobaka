import tomllib
import logging

from pydantic import BaseModel, HttpUrl, computed_field, FilePath

logger = logging.getLogger(__name__)

try:
    with open("config.toml", "rb") as f:
        config = tomllib.load(f)
    logger.debug("Loading configuration succesfull")

except:
    logger.critical("Loading configuration failed")
    exit()

class ServerConfig(BaseModel):
    base_url: HttpUrl
    login_endpoint: str
    marks_endpoint: str

    @computed_field
    @property
    def login_url(self) -> HttpUrl:
        """Full login url"""
        return self._combine_url(self.login_endpoint)
    
    @computed_field
    @property
    def marks_url(self) -> HttpUrl:
        """Full marks url"""
        return self._combine_url(self.marks_endpoint)
    
    def _combine_url(self, endpoint: str) -> HttpUrl:
        """Combine base url + endpoint"""
        return f"{self.base_url}{endpoint}" # pyright: ignore[reportReturnType]


class PathConfig(BaseModel):
    json_marks: FilePath
    results: FilePath

class AppConfig(BaseModel):
    server: ServerConfig
    path: PathConfig

appconfig = AppConfig(**config)