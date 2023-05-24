from rich import print as rprint
import socket
import shlex
import subprocess
from typing import List


def find_port() -> int:
    """
    Find a random open port
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("", 0))
    sock.listen(1)
    port = sock.getsockname()[1]
    sock.close()
    return port


def launch(ram: int, qcow: str, ign: str, ports: List[int]) -> int:
    """
    Launch FCOS with QEMU
    """

    port_list = set([])
    port_list.add(22)
    if ports is not None:
        port_list.update(ports)

    hostfwd_list = []
    port_maps = []

    for port in port_list:
        host_port = find_port()

        if port == 22:
            ssh_port = host_port

        paired_ports = f"{host_port}:{port}"
        port_maps.append(paired_ports)

        hostfwd_port = f"hostfwd=tcp::{host_port}-:{port}"
        hostfwd_list.append(hostfwd_port)

    joined_hostfwd = ",".join(hostfwd_list)

    qemu_cmd = f"qemu-system-x86_64 \
        -m {ram} \
        -enable-kvm \
        -cpu host \
        -snapshot \
        -daemonize \
        -display none \
        -drive if=virtio,file={qcow} \
        -name bupy-vm-{ssh_port} \
        -fw_cfg name=opt/com.coreos/config,file={ign} \
        -nic user,model=virtio,{joined_hostfwd}"
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
