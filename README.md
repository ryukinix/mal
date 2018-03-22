# mal - MyAnimeList Command Line Interface

[![Build Status](https://travis-ci.org/ryukinix/mal.svg?branch=master)](https://travis-ci.org/ryukinix/mal)
[![codecov](https://codecov.io/gh/ryukinix/mal/branch/master/graph/badge.svg)](https://codecov.io/gh/ryukinix/mal)
[![PyPi version](https://img.shields.io/pypi/v/mal.svg)](https://pypi.python.org/pypi/mal/)
[![Requirements Status](https://requires.io/github/ryukinix/mal/requirements.svg?branch=master)](https://requires.io/github/ryukinix/mal/requirements/?branch=master)
[![PyPi License](https://img.shields.io/pypi/l/mal.svg)](https://pypi.python.org/pypi/mal/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/mal.svg)](https://pypi.python.org/pypi/mal/)
[![PyPI status](https://img.shields.io/pypi/status/mal.svg)](https://pypi.python.org/pypi/mal/)
[![HitCount](https://hitt.herokuapp.com/ryukinix/mal.svg)](https://github.com/ryukinix/mal)


## Description

`mal` is a command-line client for the official [API](http://myanimelist.net/modules.php?go=api) of [MyAnimeList.net](http://myanimelist.net/) website.
It should remain functional indefinitely (it will never have web-scraping, unlike other alternative projects).
It is currently in alpha development and new ideas are welcome! Please check our [CONTRIBUTING.md](CONTRIBUTING.md) file.
This project was initially inspired in [pushrax/mal](https://github.com/pushrax/mal).

## Features

- Search your anime list
- Fetch your anime list
- List animes by their statuses (e.g. watching)
- Increment or decrement seen episodes
- Add animes to your watch list planner
- Edit contents of your animes on your own preferred text editor:
  tags, status, score.
- Print your MAL stats! Just like you do on MyAnimeList.

More features are currently being developed! You can also request other features [here](https://github.com/ryukinix/mal/issues).

## TL;DR | Demos

![Main Usage](https://cloud.githubusercontent.com/assets/7642878/19803847/59295fd0-9ce1-11e6-9292-7e52266de4af.gif)


![Listing Animes By Status](https://cloud.githubusercontent.com/assets/7642878/19803846/59157a9c-9ce1-11e6-93a7-30665ae859bf.gif)

## Requirements

- Python 3.4+
- [setuptools](https://pypi.python.org/pypi/setuptools/3.5.1) (For installing and developing)
- [requests](http://docs.python-requests.org/en/latest/index.html)
- [appdirs](https://pypi.python.org/pypi/appdirs)
- [decorating](https://pypi.python.org/pypi/decorating/)
- [argparse](https://docs.python.org/3.5/library/argparse.html) (Merged into stdlib since version 3.2)

Check [requirements.txt](requirements.txt) for exact versions.

## Installation

### Using pip

From the command line run:

```
pip install --user mal
```

### Manual Installation

Clone this project and inside it run:

```
pip install --user .
```

`mal` requires super-user permissions when you run `make install` outside of a `virtualenv`.
We strong encourage you to install it with `pip install --user .`.

### On ArchLinux

This project has been packaged and uploaded to the AUR as
[python-mal-git](https://aur.archlinux.org/packages/python-mal-git) in case you're using an archlinux distro.

## Usage

### Authenticating

`mal` needs your credentials in order to access your anime list. In its first call to any valid command, it will ask for your username and password and save it in **plain text** its default path (on linux `~/.config/mal/myanimelist.ini`).

The file will be saved in the following format:


```ini
[mal]
username = your_username
password = your_password

```

You may start using `mal` after authenticating your user.

### Using The Interface

When `mal` is executed without any arguments, a help message is displayed:

```
usage: mal [-h] [-v]
           {search,filter,increase,inc,decrease,dec,login,list,config,drop,stats,add,edit}
           ...

MyAnimeList command line client.

positional arguments:
  {search,filter,increase,inc,decrease,dec,login,list,config,drop,stats,add,edit}
                        commands
    search              search an anime
    filter              find anime in users list
    increase (inc)      increase anime's watched episodes by one
    decrease (dec)      decrease anime's watched episodes by one
    login               save login credentials
    list                list animes
    config              Print current config file and its path
    drop                Put a selected anime on drop list
    stats               Show anime watch stats
    add                 add an anime to the list
    edit                edit entry

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show the version of mal


```

You can also use the `-h` or `--help` options on `mal` or any of its subcommands to see specific help messages.


## Contributing

Look at [CONTRIBUTING.md](CONTRIBUTING.md)


## License

[GPLv3](LICENSE)
