from datetime import datetime

from rich import box
from rich.console import Console
from rich.table import Table

def _choose_style(average: float) -> str:
    """Choose correct color of style"""
    if average <= 2.0:
        return "bold deep_sky_blue3"
    elif average <= 3.5:
        return "bold orange_red1"
    else:
        return "bold red1"

def display_results(data: dict[str, tuple]) -> None:
    """Display results (subject and it's average)"""
    if not data:
        return

    table = Table(box=box.SIMPLE, caption=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    table.add_column("Subject")
    table.add_column("Average", style="cyan")
    table.add_column("Marks")

    for subject, description in data.items():
        style = _choose_style(description[0])
        table.add_row(subject, f"[{style}]{description[0]}[/{style}]", style_marks(description[1]))

    console = Console()
    console.print(table)

def style_marks(marks: list[tuple[float, int]]) -> str:
    """
    Conver ugly tuple to nice str output

    Example:
        [(4.0, 5), (1.5, 10)] -> '4/5, 1-/10'
    """
    final_list = []
    for mark in marks:
        final_list.append(f"{_convert_to_int(mark[0])}/{mark[1]}")
    return ", ".join(final_list)

def _convert_to_int(mark: float) -> str | int:
    """
    Convert float to int

    Example:
        1.0 -> 1
        1.5 -> 1-
    """
    if mark % int(mark) == 0.5:
        return f"{int(mark)}-"
    return int(mark)