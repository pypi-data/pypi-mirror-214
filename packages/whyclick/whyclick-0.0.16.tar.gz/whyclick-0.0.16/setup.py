#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup
import setuptools

console_scripts = """
[console_scripts]
whyclick=whyclick.cli:cli
"""

setup(
    name='whyclick',
    version='0.0.16',
    packages=['whyclick'],
    description="Cos I don't like to click",
    long_description='',
    url = 'https://github.com/alvations/whyclick',
    install_requires = ['pyderman', 'selenium>=4.10.0', 'beautifulsoup4', 'tqdm', 'requests'],
    license="MIT",
    entry_points=console_scripts,
)
