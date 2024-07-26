import pathlib
import hashlib
import inspect
import sys
import typing
import secrets

from .puzzle_data_encryption import decrypt_data, encrypt_data
from . import simple_encryption_utils as seu
from . import simple_encryption as se
from . import spiced_simple_encryption as sse
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


def _create_str(in_modules, in_objects, in_encrypted_puzzle, constants_str: str) -> str:
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
                constants_str,
                call_str,
            ]
        )
        + "\n"
    )


def _get_hasher_name(in_hasher) -> str:
    return "hashlib." + in_hasher().name


_DefaultHasher = hashlib.sha512


def _get_some_spices():
    return [secrets.token_bytes(3) for _ in range(20)]


class SimpleEncryptionConfigurator:
    def __init__(self, **kwargs):
        self._proc_hasher = kwargs.get("proc_hasher", _DefaultHasher)
        self._signature_hasher = kwargs.get("signature_hasher", _DefaultHasher)

    def get_encrypt(self):
        return se.get_encrypt(self._proc_hasher, self._signature_hasher)

    def get_needed_objects(self):
        return [
            seu.hash_bytes,
            seu.int_to_bytes,
            seu.proc_bytes,
            bu.bytestr_to_bytes,
            se.get_decrypt,
            decrypt_data,
            _run_puzzle,
        ]

    def get_constants_str(
        self,
    ) -> str:
        return (
            "_DECRYPT = get_decrypt("
            f"{_get_hasher_name(self._proc_hasher)}, "
            f"{_get_hasher_name(self._signature_hasher)})"
        )


def _list_of_bytes_to_str(in_list: typing.List[bytes]) -> str:
    return str([bu.bytes_to_bytestr(_) for _ in in_list])


def _list_of_bytes_to_codestr(in_list: typing.List[bytes]) -> str:
    raw_str = _list_of_bytes_to_str(in_list)
    return f"[bytestr_to_bytes(_) for _ in {raw_str}]"


class SpicedSimpleEncryptionConfigurator:
    def __init__(self, **kwargs):
        self._proc_hasher = kwargs.get("proc_hasher", _DefaultHasher)
        self._signature_hasher = kwargs.get("signature_hasher", _DefaultHasher)
        self._proc_spices = kwargs.get("proc_spices", _get_some_spices())
        self._signature_spices = kwargs.get("signature_spices", _get_some_spices())

    def get_encrypt(self):
        return sse.get_encrypt(
            self._proc_hasher,
            self._signature_hasher,
            self._proc_spices,
            self._signature_spices,
        )

    def get_needed_objects(self):
        return [
            seu.hash_bytes,
            seu.int_to_bytes,
            seu.proc_bytes,
            bu.bytestr_to_bytes,
            sse.get_decrypt,
            decrypt_data,
            _run_puzzle,
        ]

    def get_constants_str(
        self,
    ) -> str:
        proc_spices_str = (
            f"_PROC_SPICES = {_list_of_bytes_to_codestr(self._proc_spices)}"
        )
        signature_spices_str = (
            f"_SIGNATURE_SPICES = {_list_of_bytes_to_codestr(self._signature_spices)}"
        )
        decrypt_str = (
            "_DECRYPT = get_decrypt("
            f"{_get_hasher_name(self._proc_hasher)}, "
            f"{_get_hasher_name(self._signature_hasher)}, "
            "_PROC_SPICES, "
            "_SIGNATURE_SPICES)"
        )
        return "\n".join([proc_spices_str, signature_spices_str, decrypt_str])


def _get_configurator(**kwargs):
    encryption = kwargs.get("encryption", "spiced")
    configurators = {
        "simple": SimpleEncryptionConfigurator,
        "spiced": SpicedSimpleEncryptionConfigurator,
    }
    return configurators[encryption](**kwargs)


def create(in_puzzle, output_path: pathlib.Path, **kwargs) -> None:
    configurator = _get_configurator(**kwargs)

    encrypted_puzzle = encrypt_data(in_puzzle, configurator.get_encrypt())
    needed_modules = ["hashlib", "itertools", "base64", "json", "sys", "typing"]

    needed_objects = configurator.get_needed_objects()
    constants_str = configurator.get_constants_str()

    with open(output_path, "w", encoding="utf-8") as res_file:
        res_file.write(
            _create_str(needed_modules, needed_objects, encrypted_puzzle, constants_str)
        )
