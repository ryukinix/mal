mal -- MyAnimeList Command Line Interface
=============

[![PyPi version](https://img.shields.io/pypi/v/mal.svg)](https://pypi.python.org/pypi/mal/)
[![Requirements Status](https://requires.io/github/ryukinix/mal/requirements.svg?branch=master)](https://requires.io/github/ryukinix/mal/requirements/?branch=master)
[![PyPi License](https://img.shields.io/pypi/l/mal.svg)](https://pypi.python.org/pypi/mal/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/mal.svg)](https://pypi.python.org/pypi/mal/)
[![PyPI status](https://img.shields.io/pypi/status/mal.svg)](https://pypi.python.org/pypi/mal/)

## Description

`mal` is a command-line client for [MyAnimeList.net](http://myanimelist.net/). It uses their official [API](http://myanimelist.net/modules.php?go=api), so it should remain functional indefinitely (unlike screen-scraping alternatives). But is in alpha development yet, so new ideas is welcome! This version is a inspired tool from the slow-maintained [mal](https://github.com/pushrax/mal).

## TL;DR | Demo

![demonstration](https://i.imgur.com/f3ShSUe.gif)

## Requirements

- Python 3.0+
- [pypandoc](https://pypi.python.org/pypi/pypandoc/) (only for developing & PyPI submission)
- [requests](http://docs.python-requests.org/en/latest/index.html)

## Installation

* `sudo pip install mal`


### Manual Installation

Download the package using `git clone git@github.com:ryukinix/mal.git` or as `zip` file, so then: 

- `sudo python setup.py install`
- `sudo make install` (alternative)

For develop you can try:
- `sudo python setup.py develop`
- `sudo make develop` (alternative)

In develop mode an EGG file is linked with the actual source, that way you can try modifications and get instant feedbacks in each execution


## Usage

## First Steps

## Login

* `mal login`

![login](https://i.imgur.com/5PpIB8K.gif)

The program need your credentials to access your list. In the first call, the program will ask your `username/password` and SAVE IN PLAIN TEXT on the default_path (generally `~/.myanimelist.ini`):


```ini
[mal]
username = your_username
password = your_password

```

Why save in plain text? Because the bad design of MAL API, maybe we can change this in future, but for now you can blame her.

Now you can try any of the functionalties provide in the sequence above.


## Functionalities:

* Search in your anime list
* List anime in the sublist (e.g: watching)
* Increment/Decrement anime watching
* Score in final watching
* Fetch all anime list

## Search in your anime list 
* `mal anime-by-regex`

![search]( https://i.imgur.com/B8QNHzB.png)

## Search current anime in the sublists:

* `mal watching`
* `mal plan to watch`
* `mal rewatching`
* `mal on hold`
* `mal dropped`

![filtering](https://i.imgur.com/X1K9EyV.gif)

## Increment/Decrement
- Increment/Decrement the number of episodes watched with `mal [inc | dec] [regex]` (you can swap the order too!). If there are multiple matches, it prompts you to select which one. If incrementing from `0`, it sets the anime status to "watching" and sets the start date to today. If incrementing to the total episode count, it sets the anime status to "completed" and sets the end date to today.

* Increment:
    - `mal inc anime-regex` 
    - `mal anime-regex inc`
    - `mal +1 anime-regex`
    - `mal anime-regex +1`

* Decrement:
    - `mal dec anime-regex`
    - `mal anime-regex dec`
    - `mal -1 anime-regex`
    - `mal -1 anime-regex`


![inc-dec](https://i.imgur.com/5b1RCX6.gif)


# List all animes or any by regex

* `mal all`
* `mal list`
* `mal .+` (is regex right? :D)

![all-regex](https://i.imgur.com/KofvxNY.gif)

# License

GPLv3