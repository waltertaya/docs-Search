import os
import datetime
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt

from index_creation import build_index
from search import search_index

console = Console()

def run_cli():
    folder = "docs"
    if not os.path.exists("indexdir"):
        console.print("[bold cyan]Building index...[/bold cyan]")
        build_index(folder)

    while True:
        query = Prompt.ask("\n🔎 Enter search (or type 'exit' to quit)")
        if query.lower() == "exit":
            console.print("[yellow]Goodbye![/yellow]")
            break

        # Date filter
        date_input = Prompt.ask("📅 Filter by date (YYYY-MM-DD to YYYY-MM-DD or Enter to skip)", default="")
        start_date, end_date = None, None
        if date_input:
            try:
                parts = date_input.split("to")
                if len(parts) == 2:
                    start_date = datetime.datetime.fromisoformat(parts[0].strip())
                    end_date = datetime.datetime.fromisoformat(parts[1].strip())
            except Exception:
                console.print("[red]⚠️ Invalid date format, skipping date filter.[/red]")

        # Filetype filter
        filetype = Prompt.ask("📂 Filter by file type (pdf/docx/txt or Enter to skip)", default="").strip() or None

        matches = search_index(query, start_date, end_date, filetype)

        if matches:
            table = Table(title=f"Results for: '{query}'", show_lines=True)
            table.add_column("File", style="cyan", no_wrap=True)
            table.add_column("Type", style="magenta")
            table.add_column("Modified", style="green")
            table.add_column("Snippet", style="white")

            for fname, mod_time, ftype, snippet in matches:
                table.add_row(fname, ftype.upper(), str(mod_time.date()), snippet)

            console.print(table)
        else:
            console.print("[red]No matches found.[/red]")
