"""Typer CLI: `stats`, `dedup`, `split` commands.

Thin layer: parse args, call core modules, print output.
"""

from pathlib import Path
from typing import Annotated

import typer

from imgprep.io import scan_dataset
from imgprep.stats import class_counts

app = typer.Typer(
    no_args_is_help=True,
    help="Clean and prepare image datasets for computer vision.",
)


@app.command()
def stats(
    folder: Annotated[Path, typer.Argument(exists=True, file_okay=False)],
) -> None:
    result = scan_dataset(folder)
    for cls, count in sorted(class_counts(result).items()):
        typer.echo(f"{cls}: {count}")
    typer.echo(f"total: {len(result.valid)} valid, {len(result.corrupt)} corrupt")
    for path, reason in result.corrupt:
        typer.echo(f"corrupt: {path.relative_to(folder)} ({reason})")


@app.command()
def version() -> None:
    typer.echo("imgprep 0.1.0")
