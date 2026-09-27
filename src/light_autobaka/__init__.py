import logging

from rich.logging import RichHandler
from rich.progress import BarColumn, Progress, SpinnerColumn, TaskProgressColumn, TextColumn
from rich.traceback import install

from .calculate import calc_marks
from .config import IS_GITHUB_ACTIONS, load_config, load_credentials
from .fetch import fetch_data
from .output import create_html, display_results, export_raw_marks, export_results


def main() -> None:

    config = load_config()
    credentials = load_credentials()

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        fmt="{levelname:8} {asctime} {name} - {message}",
        datefmt="%d.%m.%Y %H:%M:%S",
        style="{",
    )
    if IS_GITHUB_ACTIONS:
        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)
        handler.setFormatter(formatter)
        root_logger.addHandler(handler)
    else:
        install()
        config.path.log.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(config.path.log, mode="w", encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
        root_logger.addHandler(RichHandler(level=logging.WARNING, rich_tracebacks=True))

    if IS_GITHUB_ACTIONS:
        marks, _ = fetch_data(config, credentials)
        averages = calc_marks(marks)
        create_html(averages, config)
    else:
        with Progress(
            SpinnerColumn(),
            TextColumn("{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            transient=True,
        ) as progress:
            task = progress.add_task("Fetching data", total=4)
            marks, raw_marks = fetch_data(config, credentials)
            progress.update(task, advance=1, description="Calculating marks")
            averages = calc_marks(marks)
            progress.update(task, advance=1, description="Exporting raw marks")
            export_raw_marks(raw_marks, config)
            progress.update(task, advance=1, description="Exporting results")
            export_results(averages, config)
            progress.update(task, advance=1)
        display_results(averages)


if __name__ == "__main__":
    main()
