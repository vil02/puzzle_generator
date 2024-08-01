import typing

from ... import bytestr_utils as bu
from ...encryption_algorithms.simple import common
from ...encryption_algorithms.simple import simple as se
from ...puzzle_data_encryption import decrypt_data
from .. import common as cc
from .common import MODULES, scrypt_params, scrypt_params_to_code_str
from ...run_puzzle import run_puzzle
from ...bytes_utils import bytes_to_int, split


class Simple:
    def __init__(self, **kwargs):
        self._scrypt_params = scrypt_params(**kwargs)
        self._signature_hasher = kwargs.get("signature_hasher", cc.DefaultHasher)

    def get_modules(self) -> typing.List[str]:
        return MODULES

    def get_encrypt(self):
        return se.get_encrypt(self._signature_hasher, self._scrypt_params)

    def get_needed_objects(self):
        return [
            common.hash_bytes,
            common.split_data_and_signature,
            common.derive_key,
            common.xor_bytes,
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
        _scrypt_params = scrypt_params_to_code_str(**self._scrypt_params)
        decrypt: str = (
            "_DECRYPT = get_decrypt("
            f"{cc.get_hasher_name(self._signature_hasher)}, "
            "_SCRYPT_PARAMS)"
        )
        return "\n".join([_scrypt_params, decrypt])
