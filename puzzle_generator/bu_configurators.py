import types
import typing

from . import bytestr_utils_64 as bu64
from . import bytestr_utils_85 as bu85


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
    return _get_bu_configurator({"base64": bu64, "base85": bu85}[encoding])
