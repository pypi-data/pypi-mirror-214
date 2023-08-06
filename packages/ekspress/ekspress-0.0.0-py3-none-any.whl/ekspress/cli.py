"""Define the CLI related functions and classes."""
from __future__ import annotations

import typer
from typing import Optional
from ekspress import __version__
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="EKSpress - An EKS Upgrade Tool")
console = Console()

def version_callback(value: bool) -> None:
    """Handle the version callback."""
    if value:
        typer.secho(f"eksupgrade version: {__version__}", fg=typer.colors.BRIGHT_BLUE, bold=True)
        raise typer.Exit()

@app.command()
def main(
    version: Optional[bool] = typer.Option(
        None, "--version", callback=version_callback, is_eager=True, help="Display the current eksupgrade version"
    ),
) -> None:
    """Handle the main entry logic."""
    pass


if __name__ == "__main__":  # pragma: no cover
    app(prog_name="ekspress")
