> MAL is currently looking for contributors. The project is primarly done in Python, but all skills and levels are welcome as there are many ways in which you can help, such as documenting, testing/opening new issues, solving bugs, developing new features and many others. If you are not sure whether your skill is or not needed, please open a new issue [here](https://github.com/ryukinix/mal/issues). Also feel free to open new issues for any bugs you find, features you think would be nice to have or questions in general.

# Steps for Contributing

- 1. Find an issue [here](https://github.com/ryukinix/mal/issues).
- 2. Verify if the chosen issue is not already in WIP (create a new issue if needed).
- 3. Mention (by commenting on the issue) that you want to take it.
- 4. Fork it and create a new branch out of `master`.
- 5. Work on it.
- 6. Submit a pull request.

# Setting up mal for development

Setup a `virtualenv` and run:


```
python -m venv venv
source venv/bin/activate
python install -r requirements.txt
python setup.py develop
```

In development mode an _EGG_ file is linked with the actual source so that you can modify and test it without the need of reinstalling it.

For more information see [Development Mode](http://setuptools.readthedocs.io/en/latest/setuptools.html#development-mode).

# Running mal without installing it

Inside the project run:

```
PYTHONPATH=. python mal/cli.py
```

PYTHONPATH variable is set to look inside the project so it will look for the local module [mal](mal/) before it looks for a installed `mal`.
