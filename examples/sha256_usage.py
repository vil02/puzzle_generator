"""Example demonstrating create_puzzles with SHA256 hashing function."""

import hashlib
from puzzle_generator.create_puzzle import create

_PUZZLE = [
    "What is 2+2?",
    "4",
    "What color is the sky?",
    "blue",
    "Great job! You've completed this SHA256-based puzzle!",
]

print(
    create(
        _PUZZLE,
        hash_function=hashlib.sha256,
        salt="custom_salt_value",
        spice="custom_spice_value",
    )
)
