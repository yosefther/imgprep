"""Typer CLI: `stats`, `dedup`, `split` commands.

Thin layer: parse args, call core modules, print output.
"""

import typer

app = typer.Typer(no_args_is_help=True)


@app.callback()
def main() -> None:
    """A command-line toolkit for cleaning and preparing image datasets."""
