"""Typer CLI: `stats`, `dedup`, `split` commands.

Thin layer: parse args, call core modules, print output.
"""

import typer

app = typer.Typer(
    no_args_is_help=True,
    help="Clean and prepare image datasets for computer vision.",
)


@app.command()
def stats(folder: str) -> None:
    typer.echo(f"would analyze {folder}")


@app.command()
def version() -> None:
    typer.echo("imgprep 0.1.0")
