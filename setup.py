# -*- coding: utf-8 -*-
from setuptools import setup

packages = ["bupy"]

package_data = {"": ["*"]}

install_requires = [
    "Jinja2>=3.1.2,<4.0.0",
    "pyxdg>=0.28,<0.29",
    "rich>=12.5.1,<13.0.0",
    "ruamel.yaml>=0.17.21,<0.18.0",
    "typer[all]>=0.6.1,<0.7.0",
    "urllib3>=1.26.10,<2.0.0",
]

entry_points = {"console_scripts": ["bupy = bupy.cli:app"]}

setup_kwargs = {
    "name": "bupy",
    "version": "0.1.1",
    "description": "A Python toolkit for Butane and Ignition",
    "author": "QuickVM",
    "author_email": "hello@quickvm.com",
    "maintainer": "QuickVM",
    "maintainer_email": "hello@quickvm.com",
    "url": "https://github.com/quickvm/bupy",
    "packages": packages,
    "package_data": package_data,
    "install_requires": install_requires,
    "entry_points": entry_points,
    "python_requires": ">=3.8.10,<4.0.0",
}


setup(**setup_kwargs)
