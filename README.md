mal -- MyAnimeList Command Line Interface
=============

[![PyPi version](https://img.shields.io/pypi/v/mal.svg)](https://pypi.python.org/pypi/mal/)
![PyPi License](https://img.shields.io/pypi/l/mal.svg)
![PyPI pyversions](https://img.shields.io/pypi/pyversions/mal.svg)
![PyPI status](https://img.shields.io/pypi/status/mal.svg)

## Description

`mal` is a command-line client for [MyAnimeList.net](http://myanimelist.net/). It uses their official [API](http://myanimelist.net/modules.php?go=api), so it should remain functional indefinitely (unlike screen-scraping alternatives). But is in alpha development yet, so new ideas is welcome! This version is a inspired tool from the slow-maintained [mal](https://github.com/pushrax/mal).

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

In develop mode an EGG file is linked with the actual source, that way you can try modifications and get instant feedbacks & at execution


## Usage

## First Steps

The program need your credentials to access your list. In the first call, the program will ask your `username/password` and SAVE IN PLAIN TEXT on the default_path (generally `~/.myanimelist.ini`):


```ini
[mal]
username = your_username
password = your_password

```

Why save in plain text? Because the bad design of MAL API, maybe we can change this in future, but for now you can blame her. You also can call directly this function:

* `mal login`

![login]( https://i.imgur.com/2boHCTq.png)

## Functionalities:

* Search in your anime list
* Search current anime in the sublist (e.g: watching)
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

![filtering](https://i.imgur.com/CP2NUF9.png)

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


![inc-dec](https://i.imgur.com/9ZF17Lh.png)


# List all animes:

* `mal all`
* `mal list`
* `mal .+` (is regex right? :D)

# License

GPLv3