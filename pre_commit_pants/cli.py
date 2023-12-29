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
        int,
        typer.Option(
            "--split", "-s", help="Pass files to Pants in batches of this size."
        ),
    ] = 1000,
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
    return_codes = []
    for i in range(0, len(files), split):
        result = subprocess.run(
            [
                "pants",
                "--unmatched-cli-globs=ignore",
                goal,
                *files[i : i + split],
            ]
        )
        return_codes.append(result.returncode)

    # If any of the Pants runs failed, exit with a non-zero code.
    if all(code == 0 for code in return_codes):
        return_code = 0
    else:
        return_code = 1

    raise SystemExit(return_code)
