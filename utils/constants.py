from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

CONFIG_PATH = PROJECT_ROOT / "config.toml"

USERNAME_ENV_TAG = "BAKA_USERNAME"
PASSWORD_ENV_TAG = "BAKA_PASSWORD"
