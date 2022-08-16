from bupy import __app_name__, __version__
from rich import print as rprint
import os
import shutil
import typer
import xdg


class SilenceTemplateException:
    def __init__(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, ex_type, ex_value, ex_traceback):
        from bupy.template import TemplateException

        if ex_type is TemplateException:
            rprint(f"[bold red]Error:[/bold red] [red]{ex_value}[/red]")
            raise typer.Abort()


def find_binary(name: str):
    """
    Finds a binary on the system by name and checks if it is executable.
    """
    binary = shutil.which(name)

    return binary


def create_xdg_config_dir(name: str) -> str:
    """
    Creates the bupy config directory in $XDG_CONFIG_HOME/bupy
    """

    directory = xdg.BaseDirectory.save_config_path(name)
    if not os.path.exists(directory):
        xdg_config_dir = os.makedirs(directory)

    return xdg_config_dir


def version_callback(value: bool) -> None:
    if value:
        rprint(f"{__app_name__}: {__version__}")
        raise typer.Exit()
