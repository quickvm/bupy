# -*- coding: utf-8 -*-
from setuptools import setup

packages = ["bupy"]

package_data = {"": ["*"]}

with open("requirements.txt") as f:
    required = f.read().splitlines()

install_requires = required

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
