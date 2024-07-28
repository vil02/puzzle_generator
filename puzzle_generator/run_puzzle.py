import sys

from .puzzle_data_encryption import decrypt_data


def run_puzzle(in_puzzle, in_decrypt, get_answer):
    print(in_puzzle["str"])
    if "rest" in in_puzzle:
        this_pass = get_answer()
        new_puzzle = decrypt_data(in_puzzle["rest"], this_pass, in_decrypt)
        if new_puzzle is None:
            print("This is a wrong answer. Try again!")
            sys.exit(1)
        else:
            run_puzzle(new_puzzle, in_decrypt, get_answer)
