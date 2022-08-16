from pathlib import Path
from subprocess import Popen, PIPE, STDOUT
import sys
import typer


# Todo: Capture stderr and do something about it
def butane_to_ignition(bu: bytes) -> bytes:
    """
    Create Ignition JSON from Butane YAML
    """
    butane = "butane"
    butane_subprocess = Popen(butane, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
    ignition_data = butane_subprocess.communicate(input=bu)[0]

    return ignition_data


def butane_encode(bu: str) -> bytes:

    if sys.stdin.isatty():
        with open(f"{bu}", "rb") as opened_file:
            butane_encoded = opened_file.read()
    else:
        butane_encoded = bu.encode()
    return butane_encoded


def butane_write(bu: bytes, file_name: str, force: bool, exit: bool) -> None:

    if not Path(file_name).is_file() or force:
        with open(f"{file_name}", "w") as f:
            f.write(bu.decode("utf-8"))
        if exit:
            raise typer.Exit(code=0)
    else:
        overwrite_it = typer.confirm(f"Overwrite {file_name}?")
        if not overwrite_it:
            raise typer.Abort()
        with open(f"{file_name}", "w") as f:
            f.write(bu.decode("utf-8"))
        if exit:
            raise typer.Exit(code=0)
