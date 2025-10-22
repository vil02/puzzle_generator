import types

import pytest

import puzzle_generator.bytestr_utils_64 as bu64
import puzzle_generator.bytestr_utils_85 as bu85

from . import utils


def _get_encode_decode_pair(in_module: types.ModuleType):
    return in_module.bytes_to_bytestr, in_module.bytestr_to_bytes


@pytest.mark.parametrize(
    "in_bytes",
    utils.BYTES_LIST,
)
@pytest.mark.parametrize(
    "encode_decode_pair", [_get_encode_decode_pair(_) for _ in (bu64, bu85)]
)
def test_bytes_to_bytestr(in_bytes: bytes, encode_decode_pair) -> None:
    bytes_to_bytestr, bytestr_to_bytes = encode_decode_pair
    bytestr = bytes_to_bytestr(in_bytes)
    assert isinstance(bytestr, str)
    assert bytestr_to_bytes(bytestr) == in_bytes
