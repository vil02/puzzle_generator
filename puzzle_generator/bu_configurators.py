import types
import typing

from .bytestr_utils import bu_b16 as bu16
from .bytestr_utils import bu_b32 as bu32
from .bytestr_utils import bu_b32hex as bu32hex
from .bytestr_utils import bu_b64 as bu64
from .bytestr_utils import bu_b85 as bu85
from .bytestr_utils import bu_standard_b64 as standard_bu64
from .bytestr_utils import bu_urlsafe_b64 as urlsafe_bu64


def _get_bu_configurator(bytes_utils_module: types.ModuleType):
    class _Configurator:
        def get_modules(self) -> list[str]:
            return ["base64"]

        def get_needed_objects(self):
            return [bytes_utils_module.bytestr_to_bytes]

        def bytes_to_bytestr(self) -> typing.Callable[[bytes], str]:
            return bytes_utils_module.bytes_to_bytestr

    return _Configurator()


def get_bu_configurator(encoding: str):
    return _get_bu_configurator(
        {
            "base16": bu16,
            "base32": bu32,
            "base32hex": bu32hex,
            "base64": bu64,
            "standard_base64": standard_bu64,
            "urlsafe_base64": urlsafe_bu64,
            "base85": bu85,
        }[encoding]
    )
