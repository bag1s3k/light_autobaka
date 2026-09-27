import json
import logging
from datetime import datetime
from pathlib import Path

from jinja2 import Template
from rich import box
from rich.console import Console
from rich.table import Table
import pytz

from .config import AppConfig


logger = logging.getLogger(__name__)
Results = dict[str, tuple[float, list[tuple[float, int]]]]


def style_marks(marks: list[tuple[float, int]]) -> str:
    def format_mark(value: float) -> str:
        if value % int(value) == 0.5:
            return f"{int(value)}-"
        return str(int(value))

    return ", ".join(f"{format_mark(mark)}/{weight}" for mark, weight in marks)


def display_results(data: Results) -> None:
    if not data:
        return
    table = Table(box=box.SIMPLE, caption=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    table.add_column("Subject")
    table.add_column("Average", style="cyan")
    table.add_column("Marks")
    for subject, (average, marks) in data.items():
        color = "deep_sky_blue3" if average <= 2 else "orange_red1" if average <= 3.5 else "red1"
        table.add_row(subject, f"[bold {color}]{average}[/bold {color}]", style_marks(marks))
    Console().print(table)


def _write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def export_raw_marks(raw_marks: list[dict], config: AppConfig) -> None:
    if raw_marks:
        _write_text(config.path.raw_marks, json.dumps(raw_marks, indent=4, ensure_ascii=False))
        logger.info("Raw marks exported to %s", config.path.raw_marks)


def export_results(data: Results, config: AppConfig) -> None:
    if data:
        _write_text(
            config.path.results,
            "".join(f"{subject:30} {result}\n" for subject, result in data.items()),
        )
        logger.info("Results exported to %s", config.path.results)


def create_html(data: Results, config: AppConfig) -> None:
    if not data:
        return
    template = Template(config.path.html_template.read_text(encoding="utf-8"))
    totals = {
        subject: (
            sum(mark * weight for mark, weight in marks),
            sum(weight for _, weight in marks),
        )
        for subject, (_, marks) in data.items()
    }
    html = template.render(
        data=data,
        marks_json=json.dumps(totals),
        title="Bakalari Averages",
        style_marks=style_marks,
        last_update=datetime.now(tz=pytz.timezone("Europe/Prague")).strftime("%Y-%m-%d %H:%M:%S"),
    )
    _write_text(config.path.html_output, html)
    logger.info("HTML created at %s", config.path.html_output)
