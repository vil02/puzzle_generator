import sys
import typing

from .puzzle_data_encryption import decrypt_data


def run_puzzle(
    in_puzzle: tuple[str, bytes],
    in_decrypt: typing.Callable[[bytes, bytes], bytes | None],
    get_answer: typing.Callable[[], str],
) -> None:
    question, rest = in_puzzle
    print(question)
    if rest:
        this_pass = get_answer()
        new_puzzle = decrypt_data(rest, this_pass, in_decrypt)
        if new_puzzle is None:
            print("This is a wrong answer. Try again!")
            sys.exit(1)
        else:
            run_puzzle(new_puzzle, in_decrypt, get_answer)


def run_puzzle_with_hints(
    in_puzzle: tuple[str, bytes],
    in_decrypt: typing.Callable[[bytes, bytes], bytes | None],
    get_answer: typing.Callable[[], str],
    proc_answer: typing.Callable[[str], str],
) -> None:
    run_puzzle(in_puzzle, in_decrypt, lambda: proc_answer(get_answer()))
