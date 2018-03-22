.. mal documentation master file, created by
   sphinx-quickstart on Tue Jan 31 12:25:51 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to mal's documentation!
===============================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

Description
-----------

``mal`` is a command-line client for the official `API <http://myanimelist.net/modules.php?go=api>`__ of `MyAnimeList.net <http://myanimelist.net/>`__ website.
It should remain functional indefinitely (it will never have web-scraping, unlike other alternative projects).
It is currently in alpha development and new ideas are welcome!
This project was initially inspired in `mal <https://github.com/pushrax/mal>`__.

Features
--------

- Search your anime list
- Fetch your anime list
- List animes by their statuses (e.g. watching)
- Increment or decrement seen episodes
- Add animes to your watch list planner
- Edit contents of your animes on your own preferred text editor:
  tags, status, score.
- Print your MAL stats! Just like you do on MyAnimeList.

More features are currently being developed!

Installation
------------

Using pip
~~~~~~~~~

From the command line run:

::

    sudo pip install mal

Manual Installation
~~~~~~~~~~~~~~~~~~~

Clone this project and inside it run:

::

    sudo python setup.py install

Or alternatively using make:

::

    pip install --user .

``mal`` requires super-user permissions when you run ``make install`` inside of a ``virtualenv``.
We strong encourage you to install it with ``pip install --user .``.

On ArchLinux
~~~~~~~~~~~~

``mal`` has been packaged and uploaded to the AUR as
`python-mal-git <https://aur.archlinux.org/packages/python-mal-git>`__
in case you're using an archlinux distro.

You may install it using an AUR wrappers such ``yaourt`` or ``pacaur``, making
the installation much simpler.

Using ``yaourt``:

::

    yaourt -S python-mal-git

Using ``pacaur``:

::

    pacaur -y python-mal-git

Or manually:

::

    wget https://aur.archlinux.org/cgit/aur.git/snapshot/python-mal-git.tar.gz
    tar xvzf python-mal-git.tar.gz
    cd python-mal-git/
    makepkg -si

Notice that all dependencies should be
installed before using this method.

Usage
-----

Authenticating
~~~~~~~~~~~~~~

`mal` needs your credentials in order to access your anime list.
In its first call to any valid command,
it will ask for your username and password and save it in **plain text** its default path (on linux ``~/.config/mal/myanimelist.ini``).

The file will be saved in the following format:

.. code:: ini

    [mal]
    username = your_username
    password = your_password

You may start using `mal` after authenticating your user.

Using The Interface
~~~~~~~~~~~~~~~~~~~

When ``mal`` is executed without any arguments a help message is
displayed:

::

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

You can also use the ``-h`` or ``--help`` options on ``mal`` or any of
its subcommands to see specific help messages.


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
