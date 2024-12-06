.. _contributing:

Contributing
============

Issues
------

This project uses the gitlab issue tracker here: https://git.astron.nl/RD/trap/-/issues.
Any issue can be raised here regarding bugs or new features.

Installing from source
----------------------

The following quick start guide assumes you are running on a unix machine.

We start by cloning from `GitLab <https://git.astron.nl/RD/trap>`_.

Then go into the folder
>>> cd trap

Now let's create and activate a venv to use:

>>> python3 -m venv venv
>>> source venv/bin/activate

Upgrade pip and install the package with the additional 'doc' and 'test' dependencies.
Here the ``-e`` flag will prevent TraP itself from being installed in the virtual environment
but should point to the source files we just checked out. This makes sure that any updates you make
to the source files will be reflected when importing the package from your virtual environment.

>>> python3 -m pip install pip
>>> python3 -m pip install -e .[doc,test]

Now your custom-build venv is ready for use!

Testing and building documentation
----------------------------------

Run the tests using pytest:

>>> python3 -m pytest tests

You can build the docs lcoally using

>>> sphinx-build docs/source build/sphinx/html -v

or if sphinx-build is not available to you,
install the ``python3-sphinx`` package on your system or try:

>>> python3 -m sphinx.cmd.build docs/source build/sphinx/html


Code formatting
---------------

`Black` and `isort` are used for code formatting.
These packages are installed when the [test] argument is used during installation (see section [Installing From Source](#installing-from-source)).
Pytest-black will test the format of the python files.
Code that does not pass the test should be reformatted using black and isort like so:

>>> python3 -m black trap tests
>>> python3 -m isort trap tests

It is recommended to install the pre-commit hook, which will check the code format on commit and fix it if needed

>>> pre-commit install

This process ensures the same code standards are enforced all over the codebase.

Merge requests
--------------

After testing and commiting your changes, check out a new branch and push it to origin.
Don't forget to make a merge request ;)
The merge request will be reviewed by one of the maintainers of the project.

Thank you for contributing!
