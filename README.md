# Bupy

The **Bu**tane **Py**thon Toolkit

Bupy was built to help users develop Butane configurations for Fedora CoreOS quickly on their workstations. It allows you to convert Butane YAML to Ignition JSON and render Butane Jinja2 templates to either Butane YAML or Ignition JSON. You can then use your Butane file or template to launch a local QEMU Virtual Machine.

### Requirements

* [Python 3.8.10^](https://www.python.org/downloads/)
* [butane](https://coreos.github.io/butane/)
* [qemu](https://www.qemu.org/download/)
* If possible, a positive attitude

### Roadmap

* [x] Convert Support

* [x] Jinja2 Template Support
* [x] Launch a local QEMU FCOS VM
* [ ] Merge Butane YAML (snippets)
* [ ] Serve Ignition JSON via HTTP
* [ ] Libvirt support

### Demo

You can watch a quick demo of Bupy on Youtube.

[![Quick demo of Bupy for Fedora CoreOS](https://img.youtube.com/vi/yBOEz827TUU/0.jpg)](https://www.youtube.com/watch?v=yBOEz827TUU)

### Development

1) Clone this repo
2) Install dependencies

```bash
poetry install
```

3) Activate a poetry shell

```bash
poetry shell
```

4) Make changes...
5) See them in action

```bash
bupy --help

 Usage: bupy [OPTIONS] COMMAND [ARGS]...

 Bupy: Butane Python toolkit.

╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --version             -v        Show the version and exit.                                                                                                                                                 │
│ --install-completion            Install completion for the current shell.                                                                                                                                  │
│ --show-completion               Show completion for the current shell, to copy it or customize the installation.                                                                                           │
│ --help                          Show this message and exit.                                                                                                                                                │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ convert                      Converts Butane YAML to Ignition JSON                                                                                                                                         │
│ template                     Renders a Jinja2 Template to Butane YAML or Ignition JSON                                                                                                                     │
│ vm                           Launches a QEMU VM with a Butane YAML or Jinja2 Template                                                                                                                      │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

 Made in ✶✶✶✶ Chicago✶✶✶✶  〜 (c) 2023 QuickVM, LLC
  ```

## License

[Apache License Version 2.0](http://www.apache.org/licenses/LICENSE-2.0>)

Copyright 2023 QuickVM, LLC
