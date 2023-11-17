# Developer Guide

## Requirements
* Python 3.8+
  * [pyenv](https://github.com/pyenv/pyenv#installation) recommended for managing python versions
* [Poetry](https://python-poetry.org/docs/) - for managing dependencies and virtual environments
* The [hub CLI tool](https://github.com/github/hub#installation) - used by the `release` scripts to open PRs in github
* Recommended IDE: [PyCharm](https://www.jetbrains.com/pycharm/download/)

## Getting Started
```shell
poetry install # sets up virtualenv and installs dependencies
make lint # check codestyle
make test # run tests
```

## Codestyle
Code should be [pythonic](https://docs.python-guide.org/writing/style/) and should conform to the
[PEP](https://peps.python.org/pep-0008/) rules enforced by
[pylint](https://pypi.org/project/pylint/).

To check codestyle at any time, run `make lint`.

## Testing
There's no explicit code coverage requirement. Contributors are expected to use their best judgement to maintain a test
suite that we're confident in, while not being so brittle as to hinder future refactors.

Monkey patching is a no-no. Instead, take advantage of dependency injection and pass mocked versions of dependencies
into the constructor of the class under test.

## Documentation
Good code is self-documenting.

However, this project uses a tool that automatically generates documentation from
docstrings.

As a result, whenever adding a new class or method that the SDK user should know about, make sure to:
* include new classes in the `__all__` list in [\_\_init\_\_.py](../../tastytrade_sdk/__init__.py), and
* include [numpy-formatted docstrings](https://numpydoc.readthedocs.io/en/latest/format.html) in new class and method
  definitions

## Submitting Changes
All work should be done on a branch and submitted for PR review.

## Releasing
When ready to release a new version of the SDK to pypi, run one of:
* `make release_patch` - for bug fixes
* `make release_minor` - for new features
* `make release_major` - for breaking changes

Each of these commands prompts you to create a new release PR in github.

**These release PRs should be approved and merged ASAP.**