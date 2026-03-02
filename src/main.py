import core.bootstrap

import logging

from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn, TimeRemainingColumn

from core.utils import ProgressConfig, display_results, get_credentials
from core.fetch import fetch_data
from core.calc import calc_marks
from core.export import export_average


logger = logging.getLogger(__name__)

with Progress(
    SpinnerColumn(),
    TextColumn("[progress.description]{task.description}"),
    BarColumn(),
    TaskProgressColumn(),
    TimeRemainingColumn(),
    transient=True
) as progress:
    
    # === SETUP FOR PROGRESS BAR == #
    STEPS = ["Load Credentials", "Fetch Data", "Calculate Marks", "Export Results"]
    config = ProgressConfig(len(STEPS), progress)

    # === LOAD LOGIN DETAILS === #
    username, password = get_credentials("BAKA_USERNAME", "BAKA_PASSWORD")
    config.update_progress()

    # === GET MARKS === #
    marks = fetch_data(username, password)
    config.update_progress()

    # === CALCULATE MARKS === #
    average = calc_marks(marks)
    config.update_progress()

    # === EXPORT RESULTS === #
    export_average(average)
    config.update_progress()

# === OUTPUT === #
display_results(average)