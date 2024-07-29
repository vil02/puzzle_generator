import typing

from ...encryption_algorithms import bytestr_utils as bu
from ...encryption_algorithms.simple import common
from ...encryption_algorithms.simple import simple as se
from ...puzzle_data_encryption import decrypt_data
from .. import common as cc
from .common import MODULES
from ...run_puzzle import run_puzzle
from ...bytes_utils import bytes_to_int, split


class Simple:
    def __init__(self, **kwargs):
        self._proc_hasher = kwargs.get("proc_hasher", cc.DefaultHasher)
        self._signature_hasher = kwargs.get("signature_hasher", cc.DefaultHasher)

    def get_modules(self) -> typing.List[str]:
        return MODULES

    def get_encrypt(self):
        return se.get_encrypt(self._proc_hasher, self._signature_hasher)

    def get_needed_objects(self):
        return [
            common.hash_bytes,
            common.int_to_bytes,
            common.split_encrypted_and_signature,
            common.proc_bytes,
            bu.bytestr_to_bytes,
            se.get_decrypt,
            bytes_to_int,
            split,
            decrypt_data,
            run_puzzle,
        ]

    def get_constants_str(
        self,
    ) -> str:
        return (
            "_DECRYPT = get_decrypt("
            f"{cc.get_hasher_name(self._proc_hasher)}, "
            f"{cc.get_hasher_name(self._signature_hasher)})"
        )
