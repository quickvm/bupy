import os
import re
import shlex
import socket
import subprocess
import typer
from rich import print as rprint
from typing import List


def find_port() -> int:
    """
    Find a random open port to use
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("", 0))
    sock.listen(1)
    port = sock.getsockname()[1]
    sock.close()
    return port


def check_port(port: int) -> bool:
    """
    Check to see if a port is available to use
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = False
    try:
        sock.bind(("", port))
        result = True
    except:
        rprint(f"[bold red]Error:[/bold red] Port {port} is already in use!")
    sock.close()
    return result


def validate_port_format(port: str) -> bool:
    """
    Validate port format. The port has to be between 1 and 65535 as a single number (8080) or a port pair (8080:80)
    """
    range_expression = r"(\d{1,4}|[1-5]\d{4}|6[0-4]\d{3}|65[0-4]\d{2}|655[0-2]\d|6553[0-5])"
    pattern = rf"^{range_expression}$|^{range_expression}:{range_expression}$"
    match = re.match(pattern, port)
    if match:
        return True
    else:
        rprint(
            f"[bold red]Error:[/bold red] The port {port} is not between 1 - 65535 and input as a single number (8080) or a port pair (8080:80)!"
        )
        raise typer.Exit(code=1)


def launch(ram: int, qcow: str, ign: str, ports: List[str]) -> int:
    """
    Launch FCOS with QEMU
    """

    hostfwd_list = []
    port_maps = []

    if not "22" or not any(port.endswith(":22") for port in ports):
        ports.append("22")

    for port in ports:
        validate_port_format(port)
        if ":" not in port:
            port = int(port)
        if isinstance(port, int):
            host_port = find_port()
            vm_port = port
        elif isinstance(port, str):
            numbers = port.split(":")
            host_port = int(numbers[0])
            vm_port = int(numbers[1])

        if not check_port(host_port):
            raise typer.Exit(code=1)

        if vm_port == 22:
            ssh_port = host_port

        paired_ports = f"{host_port}:{vm_port}"
        port_maps.append(paired_ports)

        hostfwd_port = f"hostfwd=tcp::{host_port}-:{vm_port}"
        hostfwd_list.append(hostfwd_port)

    joined_hostfwd = ",".join(hostfwd_list)

    if not os.environ.get("DISPLAY"):
        display = "-display none"
    else:
        display = ""

    qemu_cmd = f"qemu-system-x86_64 \
        -m {ram} \
        -enable-kvm \
        -cpu host \
        -snapshot \
        -daemonize \
        -drive if=virtio,file={qcow} \
        -name bupy-vm-{ssh_port} \
        -fw_cfg name=opt/com.coreos/config,file={ign} \
        -nic user,model=virtio,{joined_hostfwd} \
        {display}"
    qemu_cmd_split = shlex.split(qemu_cmd)

    rprint("Launching QEMU VM...")
    process = subprocess.Popen(qemu_cmd_split, start_new_session=True)
    qemu_pid = process.pid

    rprint(f"The PID is: {qemu_pid}")
    rprint("")
    rprint(f"The SSH port is: {ssh_port}")
    rprint(
        f"ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no core@localhost -p {ssh_port}"
    )
    rprint("")
    rprint("The port mappings are:")
    rprint("")
    for pairs in port_maps:
        rprint(pairs)
    rprint("")
    return 0
