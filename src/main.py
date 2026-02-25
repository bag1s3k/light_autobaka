from provider import fetch_data
from dotenv import load_dotenv
import os


load_dotenv()

if (username := os.getenv("BAKA_USERNAME")) is None:
    exit() # TODO: logging
if (password := os.getenv("BAKA_PASSWORD")) is None:
    exit() # TODO: logging

fetch_data(username, password)