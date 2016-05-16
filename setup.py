#!/usr/bin/env python
# coding=utf-8
#   Python Script
#
#   Copyright © Manoel Vilela
#
#

from setuptools import setup, find_packages
from codecs import open  # To use a consistent encoding
from os import path
from warnings import warn
import mal

try:
    import pypandoc
except ImportError:
    warn("Only-for-developers: you need pypandoc for upload "
         "correct reStructuredText into PyPI home page")

here = path.abspath(path.dirname(__file__))
readme = path.join(here, 'README.md')

if 'pypandoc' in globals():
    long_description = pypandoc.convert(readme, 'rst', format='markdown')
else:
    # Get the long description from the relevant file
    with open(readme, encoding='utf-8') as f:
        long_description = f.read()

setup(
    name='mal',
    version=mal.__version__,
    description="A command line interface to your MyAnimeList profile",
    long_description=long_description,
    classifiers=[
        "Environment :: Console",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Internet",
        "Topic :: Games/Entertainment",
        "Topic :: Utilities",
        "Operating System :: Unix",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
    # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='mal myanimelist cli anime manager',
    author=mal.__author__,
    author_email=mal.__email__,
    url=mal.__url__,
    download_url="{u}/archive/v{v}.tar.gz".format(u=mal.__url__,
                                                  v=mal.__version__),
    zip_safe=False,
    license='GPL',
    packages=find_packages(exclude=['ez_setup', 'examples',
                                    'tests', 'docs', '__pycache__']),
    platforms='unix',
    install_requires=[
        x.strip() for x in open('requirements.txt').readlines()
    ],
    entry_points={
        'console_scripts': [
            'mal = mal.cli:main'
        ]
    }
)
