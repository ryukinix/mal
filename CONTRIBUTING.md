# Contributing

We are looking for contributors. If you know some python and would like to help check out our [issues](https://github.com/ryukinix/mal/issues).

Also feel free to open new issues for any bug you found, features you think would be nice to have or questions in general.

# Running The Source

There are a few options to run the source in development.

# Development Mode

For developing you can run setup a virtualenv and:


```
python -m venv venv
source venv/bin/activate
python install -r requirements.txt
python setup.py develop
```

In development mode an EGG file is linked with the actual source so that way you can modify it and test without reinstalling.

For more information see [Development Mode](http://setuptools.readthedocs.io/en/latest/setuptools.html#development-mode).

# Running without need to install

Inside the project run:

```
PYTHONPATH=. python mal/cli.py
```

PYTHONPATH variable is set to look inside the project so it will look for the local module [mal](mal/) before looking for installed `mal`.
