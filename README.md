# mal - MyAnimeList Command Line Interface

[![Build Status](https://travis-ci.org/ryukinix/mal.svg?branch=master)](https://travis-ci.org/ryukinix/mal)
[![PyPi version](https://img.shields.io/pypi/v/mal.svg)](https://pypi.python.org/pypi/mal/)
[![Requirements Status](https://requires.io/github/ryukinix/mal/requirements.svg?branch=master)](https://requires.io/github/ryukinix/mal/requirements/?branch=master)
[![PyPi License](https://img.shields.io/pypi/l/mal.svg)](https://pypi.python.org/pypi/mal/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/mal.svg)](https://pypi.python.org/pypi/mal/)
[![PyPI status](https://img.shields.io/pypi/status/mal.svg)](https://pypi.python.org/pypi/mal/)
[![HitCount](https://hitt.herokuapp.com/ryukinix/mal.svg)](https://github.com/ryukinix/mal)

## Description

`mal` is a command-line client for [MyAnimeList.net](http://myanimelist.net/) which uses the official [API](http://myanimelist.net/modules.php?go=api).
It should remain functional indefinitely (unlike web-scraping alternatives).
It is currently in alpha development so new ideas are welcome!
This project is inspired from [mal](https://github.com/pushrax/mal).

## Features

* Searching your anime list
* Fetch your anime list
* List animes in certain status (e.g. watching)
* Increment or decrement episodes seen of animes

And more are currently being developed!

## TL;DR | Demos

![Main Usage](https://cloud.githubusercontent.com/assets/7642878/19803847/59295fd0-9ce1-11e6-9292-7e52266de4af.gif)


![Listing Animes By Status](https://cloud.githubusercontent.com/assets/7642878/19803846/59157a9c-9ce1-11e6-93a7-30665ae859bf.gif)

## Requirements

- Python 3.2+
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
sudo pip install mal
```

### Manual Installation

Clone this project and run inside it:

```
sudo python setup.py install
```

Or alternatively using make:

```
sudo make install
```

### On ArchLinux

If you're using the archlinux distro this project has been packaged and uploaded to
the AUR as [python-mal-git](https://aur.archlinux.org/packages/python-mal-git).

You can install it using an AUR wrappers like `yaourt` or `pacaur` which will be much simpler.

Using `yaourt`:
```
yaourt -S python-mal-git
```

Using `pacaur`:

```
pacaur -y python-mal-git
```

Or do it manually:

```
wget https://aur.archlinux.org/cgit/aur.git/snapshot/python-mal-git.tar.gz
tar xvzf python-mal-git.tar.gz
cd python-mal-git/
makepkg -si
```

Notice that before using this method all dependencies should be installed. 

## Usage

### Authenticating

The program needs your credentials to access your list. In the first call to any valid command the program will ask for your username and password and save it in **plain text** in the default path (on linux `~/.config/mal/myanimelist.ini`).

The file will be save in the following format:


```ini
[mal]
username = your_username
password = your_password

```

After authenticating you can start using the program.

### Using The Interface

When `mal` is executed without any arguments the help message is displayed:

```
usage: mal [-h]
           {search,increase,inc,decrease,dec,login,list,config,download,watch}
           ...

MyAnimeList command line client.

positional arguments:
  {search,increase,inc,decrease,dec,login,list,config,download,watch}
                        commands
    search              search an anime
    increase (inc)      increase anime's watched episodes by one
    decrease (dec)      decrease anime's watched episodes by one
    login               save login credentials
    list                list animes
    config              config - not implemented yet
    download            download - not implemented yet
    watch               watch - not implemented yet

optional arguments:
  -h, --help            show this help message and exit
```

You can also use the `-h` or `--help` options on `mal` or any of its subcommands to see specific help message.


## Contributing

We are looking for contributors. If you know some python and would like to help check out our [issues](https://github.com/ryukinix/mal/issues).

Also feel free to open new issues for any bug you found, features you think would be nice to have or questions in general.

### Running The Source

There are a few options to run the source in development.

#### Development Mode

For developing you can run:

```
sudo python setup.py develop
```

Or alternatively using make:

```
sudo make develop
```

In development mode an EGG file is linked with the actual source so that way you can modify it and test without reinstalling.

For more information see [Development Mode](http://setuptools.readthedocs.io/en/latest/setuptools.html#development-mode).

#### Running With Python

Inside the project run:

```
PYTHONPATH=. python mal/cli.py
```

PYTHONPATH variable is set to look inside the project so it will look for the local module [mal](mal/) before looking for installed `mal`.

## License

[GPLv3](LICENSE)
