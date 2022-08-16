# Bupy

The **Bu**tane **Py**thon Toolkit

Bupy was built to help users develop Butane configurations for Fedora CoreOS quickly on their workstations. It allows you to convert Butane YAML to Ignition JSON and render Butane Jinja2 templates to either Butane YAML or Ignition JSON. You can then use your Butane file or template to launch a local QEMU Virtual Machine.

### Roadmap
- [x] Convert Support
- [x] Jinja2 Template Support
- [x] Launch a local QEMU FCOS VM
- [ ] Merge Butane YAML (snippets)
- [ ] Serve Ignition JSON via HTTP
- [ ] Libvirt support


### Demo

You can watch a quick demo of Bupy on Youtube.

[![Quick demo of Bupy for Fedora CoreOS](https://img.youtube.com/vi/yBOEz827TUU/0.jpg)](https://www.youtube.com/watch?v=yBOEz827TUU)

### Development

1) Clone this repo
1) Install dependencies
  ```
  poetry install
  ```
1) Activate a poetry shell
  ```
  $ poetry shell
  Spawning shell within /home/jdoss/src/quickvm/bupy/.venv
  . /home/jdoss/src/quickvm/bupy/.venv/bin/activate
  $ . /home/jdoss/src/quickvm/bupy/.venv/bin/activate
  ```
1) Make changes...
1) See them in action
  ```
  (.venv) $ python -m bupy --help

   Usage: bupy [OPTIONS] COMMAND [ARGS]...

  ╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
  │ --version             -v        Show the version and exit.                                       │
  │ --install-completion            Install completion for the current shell.                        │
  │ --show-completion               Show completion for the current shell, to copy it or customize   │
  │                                 the installation.                                                │
  │ --help                          Show this message and exit.                                      │
  ╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
  ╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────╮
  │ convert      Converts Butane YAML to Ignition JSON                                               │
  │ merge        Merge Butane files together                                                         │
  │ qemu         Launches a QEMU VM with the specified Ignition JSON or Butane YAML                  │
  │ serve        Serve an ignition file via HTTP on a specified port                                 │
  │ template     Render Butane Jinja2 templates                                                      │
  ╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
  ```
