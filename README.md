# Gator Client
A web client for the [Gator](https://github.com/sqrl-planner/gator) API.

## Package manager
gator-client uses the [poetry](https://python-poetry.org/) package manager to manage its dependencies. To install the dependencies, run the following command:
```
poetry install
```
See the [poetry](https://python-poetry.org/) documentation for more information and
installation instructions.

<!-- ... Insert content here ... -->

## Tools

There are a number of tools available to help you with the development of sqrl. These tools ensure that your code is well-formed, follows the best practices, and
is consistent with the rest of the project.

#### Linting the codebase
- For detecting code quality and style issues, run ``flake8``
- For checking compliance with Python docstring conventions, run ``pydocstyle``

**NOTE**: these tools will not fix any issues, but they can help you identify potential problems.

#### Formatting the codebase
- For automatically formatting the codebase, run ``autopep8 --in-place --recursive .``. For more information on this command, see the [autopep8](https://pypi.python.org/pypi/autopep8) documentation.
- For automatically sorting imports, run ``isort .``

#### Running tests
For running tests, run ``pytest``.
