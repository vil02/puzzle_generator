import secrets
import typing

from ... import bytestr_utils as bu
from ...encryption_algorithms.simple import spiced as sse
from . import common as csc


def _get_some_spices():
    return [secrets.token_bytes(3) for _ in range(20)]


def _list_of_bytes_to_str(in_list: typing.List[bytes]) -> str:
    return str([bu.bytes_to_bytestr(_) for _ in in_list])


def _list_of_bytes_to_codestr(in_list: typing.List[bytes]) -> str:
    raw: str = _list_of_bytes_to_str(in_list)
    return f"[bytestr_to_bytes(_) for _ in {raw}]"


class Spiced:
    def __init__(self, **kwargs):
        self._scrypt_params = csc.scrypt_params(**kwargs)
        self._signature_params = csc.signature_params(**kwargs)
        self._proc_spices = kwargs.get("proc_spices", _get_some_spices())
        self._signature_spices = kwargs.get("signature_spices", _get_some_spices())

    def get_modules(self) -> typing.List[str]:
        return csc.MODULES

    def get_encrypt(self):
        return sse.get_encrypt(
            self._proc_spices,
            self._signature_spices,
            self._scrypt_params,
            self._signature_params,
        )

    def get_needed_objects(self):
        return csc.OBJECTS + [
            sse.get_decrypt,
        ]

    def get_constants_str(
        self,
    ) -> str:
        proc_spices: str = (
            f"_PROC_SPICES = {_list_of_bytes_to_codestr(self._proc_spices)}"
        )
        signature_spices: str = (
            f"_SIGNATURE_SPICES = {_list_of_bytes_to_codestr(self._signature_spices)}"
        )
        _scrypt_params = csc.scrypt_params_to_code_str(**self._scrypt_params)
        _signature_params = "_SIGNATURE_PARAMS = " + repr(self._signature_params)
        decrypt: str = (
            "_DECRYPT = get_decrypt("
            "_PROC_SPICES, "
            "_SIGNATURE_SPICES, "
            "_SCRYPT_PARAMS, _SIGNATURE_PARAMS)"
        )
        return "\n".join(
            [proc_spices, signature_spices, _scrypt_params, _signature_params, decrypt]
        )
