"""Typer CLI: `stats`, `dedup`, `split` commands.

Thin layer: parse args, call core modules, print output.
"""

import typer

app = typer.Typer(help="Clean and prepare image datasets for computer vision.")

@app.command()
def stats (folder:str):
    typer.echo(f"would anlize {folder}")

@app.command()
def version()->None:
    typer.echo("imgprep 0.1.0v")