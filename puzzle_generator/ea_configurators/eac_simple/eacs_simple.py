import typing

from ...encryption_algorithms.ea_simple import eas_simple
from ..check_kwargs import check_kwargs
from . import eacs_common as eacs


class EacsSimple:
    def __init__(self, bu_configurator, **kwargs) -> None:
        check_kwargs({"scrypt_params", "signature_params"}, **kwargs)
        self._bu_configurator = bu_configurator
        self._scrypt_params = eacs.scrypt_params(**kwargs)
        self._signature_params = eacs.signature_params(**kwargs)

    def get_modules(self) -> list[str]:
        return sorted(eacs.MODULES + self.bu_configurator.get_modules())

    def get_encrypt(self) -> typing.Callable[[bytes, bytes], bytes]:
        return eas_simple.get_encrypt(self._scrypt_params, self._signature_params)

    def get_needed_objects(self):
        return (
            eacs.OBJECTS
            + [
                eas_simple.get_decrypt,
            ]
            + self.bu_configurator.get_needed_objects()
        )

    def get_constants_str(
        self,
    ) -> str:
        _scrypt_params = eacs.scrypt_params_to_code_str(
            self.bu_configurator, **self._scrypt_params
        )
        _signature_params = "_SIGNATURE_PARAMS = " + repr(self._signature_params)
        decrypt: str = "_DECRYPT = get_decrypt(_SCRYPT_PARAMS, _SIGNATURE_PARAMS)"
        return "\n".join([_scrypt_params, _signature_params, decrypt])

    @property
    def bu_configurator(self):
        return self._bu_configurator
