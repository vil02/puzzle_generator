import pathlib
import hashlib
import inspect
import sys

from .puzzle_data_encryption import decrypt_data, encrypt_data
from . import simple_encryption_utils as seu
from . import simple_encryption as se
from . import bytestr_utils as bu


def _run_puzzle(in_puzzle, in_decrypt):
    print(in_puzzle["str"])
    if "rest" in in_puzzle:
        this_pass = input()
        new_puzzle = decrypt_data(
            in_puzzle["rest"], in_puzzle["hash"], this_pass, in_decrypt
        )
        if new_puzzle is None:
            print("This is a wrong answer. Try again!")
            sys.exit(1)
        else:
            _run_puzzle(new_puzzle, in_decrypt)


def _create_str(in_modules, in_objects, in_encrypted_puzzle, decrypt_str: str) -> str:
    advertisement = """# generated with puzzle-generator
#
# https://pypi.org/project/puzzle-generator/
# https://github.com/vil02/puzzle_generator
"""
    modules_str = "\n".join("import " + _ for _ in in_modules) + "\n"
    objects_str = "\n".join(inspect.getsource(_) for _ in in_objects)
    puzzle_data_str = f"_PUZZLE = {in_encrypted_puzzle}"
    call_str = "_run_puzzle(_PUZZLE, _DECRYPT)"

    return (
        "\n".join(
            [
                advertisement,
                modules_str,
                objects_str,
                puzzle_data_str,
                decrypt_str,
                call_str,
            ]
        )
        + "\n"
    )


def _get_hasher_name(in_hasher) -> str:
    return "hashlib." + in_hasher().name


def create(in_puzzle, output_path: pathlib.Path, **kwargs) -> None:
    proc_hasher = kwargs.get("proc_hasher", hashlib.sha512)
    signature_hasher = kwargs.get("signature_hasher", hashlib.sha512)
    encrypted_puzzle = encrypt_data(
        in_puzzle, se.get_encrypt(proc_hasher, signature_hasher)
    )

    needed_modules = ["hashlib", "itertools", "base64", "json", "sys", "typing"]

    needed_objects = [
        seu.hash_bytes,
        seu.int_to_bytes,
        seu.proc_bytes,
        bu.bytestr_to_bytes,
        se.get_decrypt,
        decrypt_data,
        _run_puzzle,
    ]

    decrypt_str = (
        "_DECRYPT = get_decrypt("
        f"{_get_hasher_name(proc_hasher)}, "
        f"{_get_hasher_name(signature_hasher)})"
    )

    with open(output_path, "w", encoding="utf-8") as res_file:
        res_file.write(
            _create_str(needed_modules, needed_objects, encrypted_puzzle, decrypt_str)
        )
