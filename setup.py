#!/usr/bin/env python
# coding=utf-8
#   Python Script
#
#   Copyright © Manoel Vilela
#
#

from setuptools import setup, find_packages
import mal

setup(
    name='mal',
    version=mal.__version__,
    description="A command line interface to your MyAnimeList profile",
    long_description=(
        "Personal use for managing watching animes using MyAnimeList."
        "Aimed for people whose loves doing things on terminal and hate GUIs"
    ),
    classifiers=[
        "Topic :: Internet",
        "Development Status :: 3 - ALPHA",
        "Programming Language :: Python :: 3.5",
        "Topic :: Software Development :: Build Tools",
    ],
    # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='mal myanimelist cli personal',
    author=mal.__author__,
    author_email=mal.__email__,
    url=mal.__url__,
    zip_safe=False,
    license='GPL',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests', 'docs']),
    package_dir={'build': 'mal'},
    platforms='any',
    install_requires=[
        x.strip() for x in open('requirements.txt').readlines()
    ],
    entry_points={
        'console_scripts': [
            'mal = mal.cli:main'
        ]
    }
)
