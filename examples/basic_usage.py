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

print(create(_PUZZLE))
