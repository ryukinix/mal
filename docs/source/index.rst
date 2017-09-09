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

``mal`` is a command-line client for
`MyAnimeList.net <http://myanimelist.net/>`__ which uses the official
`API <http://myanimelist.net/modules.php?go=api>`__. It should remain
functional indefinitely (unlike web-scraping alternatives). It is
currently in alpha development so new ideas are welcome! This project is
inspired from `mal <https://github.com/pushrax/mal>`__.

Features
--------

-  Searching your anime list
-  Fetch your anime list
-  List animes in certain status (e.g. watching)
-  Increment or decrement episodes seen of animes

And more are currently being developed!


Installation
------------

Using pip
~~~~~~~~~

From the command line run:

::

    sudo pip install mal

Manual Installation
~~~~~~~~~~~~~~~~~~~

Clone this project and run inside it:

::

    sudo python setup.py install

Or alternatively using make:

::

    sudo make install

On ArchLinux
~~~~~~~~~~~~

If you're using the archlinux distro this project has been packaged and
uploaded to the AUR as
`python-mal-git <https://aur.archlinux.org/packages/python-mal-git>`__.

You can install it using an AUR wrappers like ``yaourt`` or ``pacaur``
which will be much simpler.

Using ``yaourt``:

::

    yaourt -S python-mal-git

Using ``pacaur``:

::

    pacaur -y python-mal-git

Or do it manually:

::

    wget https://aur.archlinux.org/cgit/aur.git/snapshot/python-mal-git.tar.gz
    tar xvzf python-mal-git.tar.gz
    cd python-mal-git/
    makepkg -si

Notice that before using this method all dependencies should be
installed.

Usage
-----

Authenticating
~~~~~~~~~~~~~~

The program needs your credentials to access your list. In the first
call to any valid command the program will ask for your username and
password and save it in **plain text** in the default path (on linux
``~/.config/mal/myanimelist.ini``).

The file will be save in the following format:

.. code:: ini

    [mal]
    username = your_username
    password = your_password

After authenticating you can start using the program.

Using The Interface
~~~~~~~~~~~~~~~~~~~

When ``mal`` is executed without any arguments the help message is
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
its subcommands to see specific help message.




Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
