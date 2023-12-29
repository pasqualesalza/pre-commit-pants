import subprocess
from pathlib import Path
from typing import Annotated, List, Optional

import typer

from pre_commit_pants import __app_name__, __version__

# --- Typer configuration ---
app = typer.Typer()


# --- Option callbacks ---
def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}", err=True)
        raise typer.Exit()


# --- Main command ---
@app.command()
def main(
    goal: Annotated[str, typer.Argument(help="The Pants goal to run.")],
    files: Annotated[
        List[Path], typer.Argument(help="List of files to pass to Pants.")
    ],
    split: Annotated[
        Optional[int],
        typer.Option(
            "--split", "-s", help="Pass files to Pants in batches of this size."
        ),
    ] = None,
    version: Annotated[
        Optional[bool],
        typer.Option(
            "--version",
            "-v",
            help="Display the version.",
            callback=_version_callback,
            is_eager=True,
        ),
    ] = None,
) -> None:
    # Run the Pants goal on the files in batches of `split` files.
    if split is None:
        subprocess.run(["pants", goal, *files])
    else:
        for i in range(0, len(files), split):
            subprocess.run(["pants", goal, *files[i : i + split]])
