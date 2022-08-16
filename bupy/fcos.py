from collections import deque
from pathlib import Path
from rich import print as rprint
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.progress import wrap_file
import copy
import json
import lzma
import os
import shutil
import tempfile
import urllib3


class Token:
    def __init__(self, name, is_var=False) -> None:
        self.name = name
        self.is_var = is_var

    def get(self, data, args, **kwargs):

        if not self.is_var:
            return data.get(self.name, {})
        v = kwargs.get(self.name, None)
        if not v:
            v = args.popleft()
        return data.get(v, {})


class Fcos:

    lookups = {
        "disk": [
            Token("architectures"),
            Token("arch", True),
            Token("artifacts"),
            Token("platform", True),
            Token("formats"),
            Token("disk_format", True),
            Token("disk"),
        ],
        "disk_location": [
            Token(*x)
            for x in [
                ("architectures",),
                ("arch", True),
                ("artifacts",),
                ("platform", True),
                ("formats",),
                ("disk_format", True),
                ("disk",),
                ("location",),
            ]
        ],
        "disk_sha256": [
            Token(*x)
            for x in [
                ("architectures",),
                ("arch", True),
                ("artifacts",),
                ("platform", True),
                ("formats",),
                ("disk_format", True),
                ("disk",),
                ("sha256",),
            ]
        ],
    }

    def __init__(self, data):
        self._data = data

    def get_item(self, item_name, *args, **kwargs):
        cur_data = copy.deepcopy(self._data)
        deque(args)

        for item in self.lookups[item_name]:
            cur_data = item.get(cur_data, args, **kwargs)
        return cur_data

    def get_disk(self, *args, **kwargs):
        return self.get_item("disk_location", *args, **kwargs)

    def get_sha256(self, *args, **kwargs):
        return self.get_item("disk_sha256", *args, **kwargs)


def get_stream_data(
    fcos_stream="stable",
    fcos_json_url="https://builds.coreos.fedoraproject.org/streams/",
):
    """
    Grabs FCOS stream data off a URL
    """
    http = urllib3.PoolManager()
    resp = http.request("GET", fcos_json_url + fcos_stream + ".json")
    fcos_stream_data = json.loads(resp.data)

    return fcos_stream_data


def libvirt_image_path(libvirt_image_path=None):

    if libvirt_image_path is not None:
        local_libvirt_image_path = libvirt_image_path
    else:
        home = str(Path.home())
        libvirt_image_path = "/.local/share/libvirt/images"
        local_libvirt_image_path = home + libvirt_image_path
    return local_libvirt_image_path


# TODO: Add list disks support
# def list_disks():
#     fcos_disks =
#     for path in os.scandir(dir_path):
#         if path.is_file():
#             rprint(path.name)

# TODO: If you ctrl+c in the middle of the extract it leaves a incomplete VM qcow2 file. We should clean that up if we exit in the middle of an extraction
def download_disk(download_url, download_path=None):
    """
    Download and verify FCOS disk image
    """

    if download_path is not None:
        download_path = download_path
    else:
        download_path = libvirt_image_path()

    archive_name = os.path.basename(download_url)
    disk_name = os.path.splitext(archive_name)[0]
    disk_path = download_path + "/" + disk_name

    if not os.path.exists(download_path):
        os.makedirs(download_path, mode=0o775)
        rprint(download_path + " does not exist. Creating it!")

    if os.path.exists(disk_path):
        rprint(disk_path + " already exists. Skipping download!")
        rprint("")
    else:
        with tempfile.TemporaryDirectory() as tmpdirname:

            archive_path = tmpdirname + "/" + archive_name
            http = urllib3.PoolManager()
            download_file = http.request("GET", download_url, preload_content=False)
            download_size = int(download_file.headers["Content-Length"])

            with wrap_file(
                download_file,
                download_size,
                description=f"Downloading {archive_name}",
            ) as req:
                with open(archive_path, "wb") as out_file:
                    shutil.copyfileobj(req, out_file)

            with Progress(
                TextColumn("[progress.description]{task.description}"),
                SpinnerColumn(),
                transient=True,
            ) as progress:
                progress.add_task(description=f"Extracting {archive_name}...", total=None)
                with lzma.open(archive_path) as archive_content:
                    with open(disk_path, "wb") as write_disk:
                        shutil.copyfileobj(archive_content, write_disk)
            rprint(f"Extracting {archive_name}... Done!")

    return disk_path
