import logging
import os
from rich.traceback import install
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from dotenv import load_dotenv
from log import logging_setup

# Intialization
install()
logging_setup()
load_dotenv()

from fetch import fetch_data
from calc import calc_marks
from export import export_average
from progress import current_task


logger = logging.getLogger(__name__)

with Progress(
    SpinnerColumn(),
    TextColumn("[progress.description]{task.description}"),
    BarColumn(),               # Samotná čára
    TaskProgressColumn(),      # Procenta
) as progress:

    total_task = 4
    task = current_task()
    run = progress.add_task("", total=total_task)

    # === LOAD LOGIN DETAILS === #
    if (username := os.getenv("BAKA_USERNAME")) is None:
        logger.critical("Failed to load username")
        exit()
    if (password := os.getenv("BAKA_PASSWORD")) is None:
        logger.critical("Failed to load password")
        exit()
    logger.info("Login details loaded successful")
    progress.update(run, advance=1, description=f"{next(task)}/{total_task}")

    # === GET MARKS === #
    marks = fetch_data(username, password)
    progress.update(run, advance=1, description=f"{next(task)}/{total_task}")

    # === CALCULATE MARKS === #
    average = calc_marks(marks)
    progress.update(run, advance=1, description=f"{next(task)}/{total_task}")

    # === EXPORT RESULTS === #
    export_average(average)
    progress.update(run, advance=1, description=f"{next(task)}/{total_task}")