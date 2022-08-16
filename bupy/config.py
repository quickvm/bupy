import os
import typer
import yaml

from bupy import (
 __app_name__
)

home_dir = str(Path.home())
libvirt_image_dir = os.path.join(home_dir, '/.local/share/libvirt/images')

default_config = [__app_name__]


def intialize_app():
    """
    Initialize config directory/file and ensure that
    $HOME/.local/share/libvirt/images exists
    """
    config_dir = xdg.save_config_path(__app_name__)
    config_file = os.path.join(config_dir, 'config.yaml')

    if not

    if not os.path.exists(libvirt_image_dir):
        os.makedirs(libvirt_image_dir)


def _create_config_file(config_dir: str) -> str:
    try:
        with config_dir.open("w") as file:
            config_parser.write(file)
    except OSError:
        return DB_WRITE_ERROR
    return SUCCESS
