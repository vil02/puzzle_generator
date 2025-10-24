"""
This file illustrates how one can reduce the output size
by using base85 encoding.

The default encoding is base64.
"""

from puzzle_generator.create_puzzle import create

_PUZZLE = [
    "What is 1+1?",
    "2",
    "What is my name?",
    "Piotr",
    "Congratulations, you solved this quiz!",
]

# note that the encoding is set to base85
print(create(_PUZZLE, encoding="base85"))
