# mal - MyAnimeList Command Line Interface

[![Build Status](https://travis-ci.org/ryukinix/mal.svg?branch=master)](https://travis-ci.org/ryukinix/mal)
[![codecov](https://codecov.io/gh/ryukinix/mal/branch/master/graph/badge.svg)](https://codecov.io/gh/ryukinix/mal)
[![PyPi version](https://img.shields.io/pypi/v/mal.svg)](https://pypi.python.org/pypi/mal/)
[![PyPi License](https://img.shields.io/pypi/l/mal.svg)](https://pypi.python.org/pypi/mal/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/mal.svg)](https://pypi.python.org/pypi/mal/)
[![PyPI status](https://img.shields.io/pypi/status/mal.svg)](https://pypi.python.org/pypi/m

## Description

`mal` is a command-line client for [MyAnimeList](http://myanimelist.net/), via the [official API](http://myanimelist.net/modules.php?go=api).

One of the major design goals of this project is to avoid the use of web-scraping, which means it should work indefinitely. Other projects
that scrape the website tend to break whenever MyAnimeList has an update, rarely ever recovering from the needed maintenance as a result.

Development is currently in alpha. New ideas are welcome! But please check [CONTRIBUTING.md](CONTRIBUTING.md) before you submit that pull
request.

This project is an unofficial fork of [pushrax/mal](https://github.com/pushrax/mal), which seems to have fallen out of maintenance.

## Features

- Search your anime list.
- Fetch your anime list.
- List animes by their status (e.g. `watching`).
- Increment or decrement episode watch count.
- Add anime to your `Plan To Watch` list.
- Edit anime metadata (currently `tags`, `status` and `score`) using your favorite text editor.
- Print your MAL stats! Just like you do on MyAnimeList.

More features are currently being developed! 

If you have a suggestion for a new feature, a bug to report or something else, you can submit an [issue](https://github.com/ryukinix/mal/issues).

Please note that as this project is still in alpha development, pretty much everything is subject to change.

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

See [requirements.txt](requirements.txt) for detailed version information.

## Installation

### Preface

Ensure that you are using **Python 3** before attempting to install.

It's common for systems to have both Python 2 and 3, so if necessary, use `pip3` or `python3 -m pip`.

If your system has both `python2` and `python3`, replace all instances of `python` and `pip` with `python3` and `pip3` (or `python3 -m pip`).

### Install via `pip`

From the command line, run:

    $ pip install --user mal

This will install the latest stable build of `mal` from the `PyPi` repository.

### Manual Installation

If you want the absolute latest, bleeding-edge version, you'll have to install manually.

Clone this project and run `pip`:

    $ git clone https://github.com/ryukinix/mal
    $ cd mal
    $ sudo pip install --user .

Note: If installing in a `virtualenv`, the `sudo` is not necessary.

It's also possible to install with the makefile (`sudo make install`) and the setup script (`sudo python3 ./setup.py install`),
but we strongly recommend `pip`, as it tracks dependencies, and can uninstall. It *is* a package manager, after all.

Finally, if you want to update after having already installed, you can do this:

    $ git pull origin master
    $ sudo pip install --user .

### On Arch Linux

This project has been packaged and uploaded to the AUR as
[python-mal-git](https://aur.archlinux.org/packages/python-mal-git) in case you're using Arch Linux or a similar distro (like Manjaro).

### Troubleshooting

If you just *can't* get `mal` to run because it's crashing upon startup, make sure that everything is using `python3`

    $ head -1 $(which mal)
    #!/usr/bin/python
    $ sudo ed $(which mal) <<< $'1s/python$/python3\nwq'
    28
    #!/usr/bin/python3
    29
    $ head -1 $(which mal)
    #!/usr/bin/python3

You might have to go through a few files to get it to work, but usually, editing the launcher is enough. Failing that,
delete the launcher, re-clone the repo, and try again in a `virtualenv`. If it works there, be careful to follow the above steps and
make sure you're using python3 for everything.

## Usage

### Authenticating

For some reason, the MAL API requires a username and password for most actions... including searching the main database. Thus, `mal` needs
your MAL login to be useful. To prevent this from being a headache, `mal` stores your credentials in your OS's default config path
(e.g. `~/.config/mal/myanimelist.ini` for Linux). Your username and password are stored unencrypted in **plain text** in that file. 
If you haven't already authenticated (`mal login`), the program will ask for your credentials when needed.

Currently, there is an [open issue](https://github.com/ryukinix/mal/issues/81) hoping to resolve the whole "plain text password" kerfuffle.

The format of `myanimelist.ini` is as follows:

```ini
[mal]
username = your_username
password = your_password

```

### Using The Interface

When `mal` is executed without any arguments, a help message is displayed:

    $ mal
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

You can also use the `-h` or `--help` options with `mal` or any of its subcommands to see specific help messages.

    $ mal list -h
    usage: mal list [-h] [--extend] [--user USER] [section]

    positional arguments:
      section      section to display, can be one of: [all, watching, completed,
                   on hold, dropped, plan to watch, rewatching] (default: all)

    optional arguments:
      -h, --help   show this help message and exit
      --extend     display extra info such as start/finish dates and tags
      --user USER  choose which users list to show

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)

## License

[GPLv3](LICENSE)
