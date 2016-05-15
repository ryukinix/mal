###
mal
###

`mal` is a command-line client for MyAnimeList.net_. It uses their official API_, so it should remain functional indefinitely (unlike screen-scraping alternatives).

.. _MyAnimeList.net: http://myanimelist.net/
.. _API: http://myanimelist.net/modules.php?go=api

Installation
------------

- `sudo python setup.py install`


Requirements
------------

- Python 3.0+
- requests_

.. _requests: http://docs.python-requests.org/en/latest/index.html

Usage
-----

Currently `mal` has this functionality:

- Search your anime list with `mal [regex]`
- Search your current anime list with
- Increment the number of episodes watched with `mal inc [regex]`. If there are multiple matches, it prompts you to select which one. If incrementing from 0, it sets the anime status to "watching" and sets the start date to today. If incrementing to the total episode count, it sets the anime status to "completed" and sets the end date to today.
- An equivalent functionality was added to `dec` too, so you can `mal dec [regex]`

More should be coming eventually.
