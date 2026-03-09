from pydantic import BaseModel

from config.models.path_config import PathConfig
from config.models.server_config import ServerConfig

class AppConfig(BaseModel):
    server: ServerConfig
    path: PathConfig
