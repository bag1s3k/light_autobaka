from log import logging_setup
logging_setup()
from log import logging_setup

from fetch import fetch_data
from dotenv import load_dotenv
import os
import logging

load_dotenv()

logger = logging.getLogger(__name__)

if (username := os.getenv("BAKA_USERNAME")) is None:
    logger.error("Failed to load username")
    exit()
if (password := os.getenv("BAKA_PASSWORD")) is None:
    logger.error("Failed to load password")
    exit()

marks = fetch_data(username, password) # pyright: ignore[reportArgumentType]
# print(marks)