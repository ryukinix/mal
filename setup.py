#!/usr/bin/env python
# coding=utf-8
#   Python Script
#
#   Copyright © Manoel Vilela
#
#

from setuptools import setup, find_packages

version = '0.1'

setup(
    name='mal',
    version=version,
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
    author='Manoel Vilela',
    zip_safe=False,
    author_email='manoel_vilela@engineer.com',
    url='https://github.com/ryukinix/mal',
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
