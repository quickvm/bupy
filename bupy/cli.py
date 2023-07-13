from bupy import butane, fcos, qemu, util, __app_name__, __version__
from bupy import template as tpl
from pathlib import Path
from rich import print as rprint
from rich import print_json
from rich.syntax import Syntax
from rich.console import Console
from tempfile import NamedTemporaryFile
from typing import List, Optional
import sys
import time
import typer


app = typer.Typer(
    help="[bold]Bupy:[/bold] [bold]Bu[/bold]tane [bold]Py[/bold]thon toolkit.",
    rich_markup_mode="rich",
    no_args_is_help=True,
    epilog="Made in [pale_turquoise1]✶✶✶✶[/pale_turquoise1] [red1]Chicago[/red1][pale_turquoise1]✶✶✶✶[/pale_turquoise1]  〜 (c) 2023 QuickVM, LLC",
    pretty_exceptions_show_locals=False,
)


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the version and exit.",
        callback=util.version_callback,
        is_eager=True,
    )
) -> None:
    return


@app.command()
def convert(
    file: str = typer.Argument(
        ... if sys.stdin.isatty() else sys.stdin.read().strip(),
        help="Reads Butane from a file or stdin and converts it to Ignition JSON.",
    ),
    write: str = typer.Option("", "--write", "-w", help="Write the Ignition JSON to a file."),
    force: bool = typer.Option(False, "--force", "-f", help="Overwrite an existing Ignition file."),
    pretty: bool = typer.Option(
        False, "--pretty", "-p", help="Makes the Ignition JSON pretty. Sooo pretty..."
    ),
):
    """
    Converts Butane YAML to Ignition JSON
    """
    butane_binary = util.find_binary("butane")

    if butane_binary is None:
        rprint(
            "[bold red]Error:[/bold red] The butane binary could not be found! Please [link=https://coreos.github.io/butane/getting-started/]install[/link] it."
        )
        raise typer.Exit(code=1)

    butane_file = butane.butane_encode(file)

    ignition_json = butane.butane_to_ignition(butane_file)

    if write:
        butane.butane_write(ignition_json, file, force, True)
    if pretty:
        print_json(ignition_json.decode("utf-8"))
    else:
        if sys.stdout.isatty():
            rprint(ignition_json.decode("utf-8"))
        else:
            print(ignition_json.decode("utf-8"))


# @app.command()
# def merge():
#     """
#     Merges Butane files together
#     """
#     typer.echo("Merging Butane files...")


@app.command()
def vm(
    file: str = typer.Argument(
        ... if sys.stdin.isatty() else sys.stdin.read().strip(),
        help="Reads Butane from a file or stdin and converts it to Ignition JSON.",
        show_default=False,
    ),
    template: str = typer.Option(
        "",
        "--template",
        "-t",
        help="Read file as a Jinja2 template and load a variables file.\n(--template bupyvars.yaml template.bu.j2)",
    ),
    write: str = typer.Option("", "--write", "-w", help="Write the Ignition JSON to a file."),
    force: bool = typer.Option(False, "--force", "-f", help="Overwrite an existing Ignition file."),
    stream: str = typer.Option(
        "stable",
        "--stream",
        "-s",
        help="Fedora CoreOS Stream: stable, testing, next",
    ),
    arch: str = typer.Option(
        "x86_64",
        "--arch",
        "-a",
        help="Fedora CoreOS arch: aarch64, s390x, x86_64",
    ),
    ram: int = typer.Option(1024, "--ram", "-r", help="RAM amount in MB"),
    ports: Optional[List[str]] = typer.Option(
        None,
        "--port",
        "-p",
        help="Pass a single port number (8080) to map a random host port to the VM port. Pass 8080:80 to assign a static host port to the VM port. The --port option can be used many times. The port range allowed is 1 - 65535.",
    ),
):
    """
    Launches a QEMU VM with a Butane YAML or Jinja2 Template
    """

    butane_binary = util.find_binary("butane")
    qemu_binary = util.find_binary("qemu-system-x86_64")

    if butane_binary is None:
        rprint(
            "[bold red]Error:[/bold red] The butane binary could not be found! Please [link=https://coreos.github.io/butane/getting-started/]install[/link] it."
        )
        raise typer.Exit(code=1)

    if qemu_binary is None:
        rprint(
            "[bold red]Error:[/bold red] The qemu-kvm binary could not be found! Please [link=https://www.qemu.org/download/]install[/link] it."
        )
        raise typer.Exit(code=1)

    # Download FCOS image and stick it in ~/.local/share/libvirt/images
    # TODO: move this to fcos.py and add download flags
    home = str(Path.home())
    libvirt_image_path = "/.local/share/libvirt/images"
    local_fcos_download_path = home + libvirt_image_path
    fcos_stream_data = fcos.get_stream_data(stream)
    fcos_download_url = fcos.Fcos(fcos_stream_data).get_disk(
        arch=arch, platform="qemu", disk_format="qcow2.xz"
    )
    fcos_disk = fcos.download_disk(fcos_download_url, local_fcos_download_path)

    if template:
        with util.SilenceTemplateException():
            butane_file = tpl.rendered_template(file, tpl.read_template_vars(template))
    else:
        butane_file = butane.butane_encode(file)

    ignition_json = butane.butane_to_ignition(butane_file)

    if write:
        butane.butane_write(ignition_json, file, force, False)

    ignition_launch_file = NamedTemporaryFile(delete=False, suffix=".ign")
    ignition_launch_file_path = ignition_launch_file.name

    with open(ignition_launch_file_path, "wb") as ignition_launch_file:
        ignition_launch_file.write(ignition_json)

    qemu.launch(ram, fcos_disk, ignition_launch_file_path, ports)
    rprint("VM Launched! :rocket:")
    time.sleep(2)
    Path(ignition_launch_file_path).unlink()


# @app.command()
# def serve():
#     """
#     Serve an Ignition file via HTTP on a specified port
#     """
#     typer.echo("Coming soon...")


@app.command()
def template(
    template: str = typer.Argument(
        ... if sys.stdin.isatty() else sys.stdin.read().strip(),
        help="Reads a Jinja2 template from a file or stdin, renders the template and converts it to Ignition JSON.",
        show_default=False,
    ),
    variables: str = typer.Argument(
        ...,
        help="Reads a YAML file to use as variables for rendering a Jinja2 template.",
    ),
    show: bool = typer.Option(
        False, "--show", "-s", help="Print the rendered template.", show_default=False
    ),
    line_numbers: bool = typer.Option(
        True, "--numbers", "-n", help="Show line numbers in printed template."
    ),
    write: str = typer.Option("", "--write", "-w", help="Write the Ignition JSON to a file."),
    force: bool = typer.Option(False, "--force", "-f", help="Overwrite an existing Ignition file."),
    pretty: bool = typer.Option(
        False, "--pretty", "-p", help="Makes the Ignition JSON pretty. Very pretty..."
    ),
):
    """
    Renders a Jinja2 Template to Butane YAML or Ignition JSON
    """
    butane_binary = util.find_binary("butane")

    if butane_binary is None:
        rprint(
            "[bold red]Error:[/bold red] The butane binary could not be found! Please [link=https://coreos.github.io/butane/getting-started/]install[/link] it."
        )
        raise typer.Exit(code=1)

    with util.SilenceTemplateException():
        if show:
            bu = tpl.rendered_template(template, tpl.read_template_vars(variables)).decode("utf-8")
            if sys.stdout.isatty():
                syntax = Syntax(bu, "YAML", line_numbers=line_numbers)
                console = Console(color_system=None)
                console.print(syntax)
            else:
                print(bu)
            raise typer.Exit()

        # TODO: Add support for finding bupyvars.yaml file in CWD, or in the directory the template resides in.
        # cwd = Path.cwd()
        template_output = tpl.rendered_template(template, tpl.read_template_vars(variables))
        ignition_json = butane.butane_to_ignition(template_output)

    if write:
        butane.butane_write(ignition_json, write, force, True)
    if pretty:
        print_json(ignition_json.decode("utf-8"))
    else:
        if sys.stdout.isatty():
            rprint(ignition_json.decode("utf-8"))
        else:
            print(ignition_json.decode("utf-8"))
