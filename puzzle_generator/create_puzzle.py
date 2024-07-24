import pathlib
import inspect
import sys

from .puzzle_data_encryption import decrypt_data, encrypt_data
from . import simple_encryption_utils as seu
from . import bytestr_utils as bu


def _run_puzzle(in_puzzle, in_decrypt_str):
    print(in_puzzle["str"])
    if "rest" in in_puzzle:
        this_pass = input()
        new_puzzle = decrypt_data(
            in_puzzle["rest"], in_puzzle["hash"], this_pass, in_decrypt_str
        )
        if new_puzzle is None:
            print("This is a wrong answer. Try again!")
            sys.exit(1)
        else:
            _run_puzzle(new_puzzle, in_decrypt_str)


def _create_str(in_modules, in_functions, in_encrypted_puzzle):
    advertisement = """# generated with puzzle-generator
#
# https://pypi.org/project/puzzle-generator/
# https://github.com/vil02/puzzle_generator
"""
    modules_str = "\n".join("import " + _ for _ in in_modules) + "\n"
    functions_str = "\n".join(inspect.getsource(_) for _ in in_functions)
    puzzle_data_str = f"_PUZZLE = {in_encrypted_puzzle}"
    call_str = "_run_puzzle(_PUZZLE, decrypt_str)"

    return (
        "\n".join(
            [advertisement, modules_str, functions_str, puzzle_data_str, call_str]
        )
        + "\n"
    )


def create(in_puzzle, output_path: pathlib.Path) -> None:
    encrypted_puzzle = encrypt_data(in_puzzle, seu.encrypt_str)

    needed_modules = ["hashlib", "itertools", "base64", "json", "sys"]

    needed_functions = [
        seu.hash_bytes,
        seu.int_to_bytes,
        seu.proc_bytes,
        seu.decrypt_bytes,
        bu.bytestr_to_bytes,
        seu.decrypt_str,
        decrypt_data,
        _run_puzzle,
    ]

    with open(output_path, "w", encoding="utf-8") as res_file:
        res_file.write(_create_str(needed_modules, needed_functions, encrypted_puzzle))
