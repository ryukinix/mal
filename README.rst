###
mal
###

``mal`` is a command-line client for MyAnimeList.net_. It uses their official API_, so it should remain functional indefinitely (unlike screen-scraping alternatives).

.. _MyAnimeList.net: http://myanimelist.net/
.. _API: http://myanimelist.net/modules.php?go=api

Requirements
------------

- Python 3.0+
- requests_

.. _requests: http://docs.python-requests.org/en/latest/index.html

Configuration
-------------

First, create ``~/.myanimelist.ini`` and fill it with your MAL account details:

.. code:: ini

    [mal]
    username = your_username
    password = your_password


Yes, it's stored plain text, blame MAL's poor API.

Usage
-----

Currently ``mal`` has rather limited functionality:

- Search your anime list with ``mal [regex]``
- Increment the number of episodes watched with ``mal inc [regex]``. If there are multiple matches, it prompts you to select which one. If incrementing from 0, it sets the anime status to "watching" and sets the start date to today. If incrementing to the total episode count, it sets the anime status to "completed" and sets the end date to today.

More should be coming eventually.
