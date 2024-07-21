import pathlib

from puzzle_generator.create_puzzle import create

_PUZZLE = {
    "str": "What is 1+1?",
    "pass": "2",
    "rest": {
        "str": "What is my name?",
        "pass": "Piotr",
        "rest": {"str": "Congratulations, you solved this quiz!"},
    },
}

create(_PUZZLE, pathlib.Path("example_puzzle.py"))
