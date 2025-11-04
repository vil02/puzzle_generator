# About `puzzle_generator`

[![PyPI version](https://badge.fury.io/py/puzzle-generator.svg)](https://pypi.org/project/puzzle-generator/)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=vil02_puzzle_generator&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=vil02_puzzle_generator)
[![codecov](https://codecov.io/gh/vil02/puzzle_generator/graph/badge.svg?token=C4HUFJ9QJH)](https://codecov.io/gh/vil02/puzzle_generator)
[![CodeFactor](https://www.codefactor.io/repository/github/vil02/puzzle_generator/badge)](https://www.codefactor.io/repository/github/vil02/puzzle_generator)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/0f53341a63914f1f9656782bff0e5089)](https://app.codacy.com/gh/vil02/puzzle_generator/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)
[![OpenSSF Scorecard](https://api.securityscorecards.dev/projects/github.com/vil02/puzzle_generator/badge)](https://securityscorecards.dev/viewer/?uri=github.com/vil02/puzzle_generator)

Basic functionality of [`puzzle_generator`](./puzzle_generator) is to generate
a single python file representing a puzzle or quiz.
The upcoming questions are stored in an encrypted form,
so it is _difficult_ to read them before providing correct answers.
The generated file does not have any external dependencies.

## Getting started

This package is available at [PyPI](https://pypi.org/project/puzzle-generator/).
It can be installed using the command

```shell
pip install puzzle-generator
```

[`examples`](./examples) show some basic usage.

## Information for developers

The project is setup using [poetry](https://python-poetry.org/).
In order to create a _development environment_,
after cloning this repository, run the command:

```shell
poetry install --with dev
```

If you just want to see the examples in action,
it is enough to clone this repository and run the command:

```shell
poetry install
```

Afterwards you can execute the commands like:

```shell
poetry run python3 examples/basic_usage.py
```
