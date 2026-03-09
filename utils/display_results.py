from rich import box
from rich.console import Console
from rich.table import Table

def display_results(data: dict[str, float]) -> None:
    """Display results (subject and it's average)"""
    if not data:
        return

    table = Table(box=box.SIMPLE)
    table.add_column("Subject")
    table.add_column("Average", style="cyan")

    for s, a in data.items():
        table.add_row(s, str(a))

    console = Console()
    console.print(table)