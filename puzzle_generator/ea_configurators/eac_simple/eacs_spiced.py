import secrets
import typing

from ...encryption_algorithms.ea_simple import eas_spiced
from ..check_kwargs import check_kwargs
from . import eacs_common as eacs


def _get_some_spices() -> list[bytes]:
    return [secrets.token_bytes(3) for _ in range(20)]


def _list_of_bytes_to_str(bytes_to_bytestr, in_list: list[bytes]) -> str:
    return str([bytes_to_bytestr(_) for _ in in_list])


def _list_of_bytes_to_codestr(bytes_to_bytestr, in_list: list[bytes]) -> str:
    raw: str = _list_of_bytes_to_str(bytes_to_bytestr, in_list)
    return f"[bytestr_to_bytes(_) for _ in {raw}]"


class EacsSpiced:
    def __init__(self, bu_configurator, **kwargs) -> None:
        check_kwargs(
            {"scrypt_params", "signature_params", "proc_spices", "signature_spices"},
            **kwargs,
        )
        self._bu_configurator = bu_configurator
        self._scrypt_params = eacs.scrypt_params(**kwargs)
        self._signature_params = eacs.signature_params(**kwargs)
        self._proc_spices = kwargs.get("proc_spices", _get_some_spices())
        self._signature_spices = kwargs.get("signature_spices", _get_some_spices())

    def get_modules(self) -> list[str]:
        return sorted(eacs.MODULES + self.bu_configurator.get_modules())

    def get_encrypt(self) -> typing.Callable[[bytes, bytes], bytes]:
        return eas_spiced.get_encrypt(
            self._proc_spices,
            self._signature_spices,
            self._scrypt_params,
            self._signature_params,
        )

    def get_needed_objects(self):
        return (
            eacs.OBJECTS
            + [
                eas_spiced.must_be_nonempty,
                eas_spiced.get_decrypt,
            ]
            + self.bu_configurator.get_needed_objects()
        )

    def get_constants_str(
        self,
    ) -> str:
        _bytes_to_bytestr = self.bu_configurator.bytes_to_bytestr()
        proc_spices: str = (
            "_PROC_SPICES = "
            f"{_list_of_bytes_to_codestr(_bytes_to_bytestr, self._proc_spices)}"
        )
        signature_spices: str = (
            "_SIGNATURE_SPICES = "
            f"{_list_of_bytes_to_codestr(_bytes_to_bytestr, self._signature_spices)}"
        )
        _scrypt_params = eacs.scrypt_params_to_code_str(
            self._bu_configurator, **self._scrypt_params
        )
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

    @property
    def bu_configurator(self):
        return self._bu_configurator
