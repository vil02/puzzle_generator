# About `puzzle_generator`

Basic functionality of [`puzzle_generator`](./puzzle_generator) is to generate
a single python file representing a puzzle or quiz.
The answers and the upcoming questions are encrypted.
The generated file does not have eny external dependencies.

## Getting started

This package is available at [PyPI](https://pypi.org/project/puzzle-generator/).
It can be installed using the command

```shell
pip install puzzle-generator
```

[`examples`](./examples) show some basic usage.

## Information for developers

The project is setup using [poetry](https://python-poetry.org/).
In order to create a _develompent enviroment_,
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
