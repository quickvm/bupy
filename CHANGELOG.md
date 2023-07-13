# CHANGELOG

## 0.1.2

* Update Typer to 0.9.0 and Rich to 13.4.2.

IMPROVEMENTS:

* Add support for static port maps when launching a VM with QEMU. See bupy vm --help for more info.
* Check for DISPLAY in the env and set -display none on QEMU if running on a headless server.
* Detect if we are sending Template output to a TTY or not

## 0.1.1

IMPROVEMENTS:

* Python 3.8.10^ support.

## 0.1.0

* Initial release!
