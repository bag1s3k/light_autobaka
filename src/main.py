import logging
import os
from dotenv import load_dotenv
from log import logging_setup

# Intialization
logging_setup()
load_dotenv()

from fetch import fetch_data



logger = logging.getLogger(__name__)

if (username := os.getenv("BAKA_USERNAME")) is None:
    logger.error("Failed to load username")
    exit()
if (password := os.getenv("BAKA_PASSWORD")) is None:
    logger.error("Failed to load password")
    exit()

marks = fetch_data(username, password)
# print(marks)