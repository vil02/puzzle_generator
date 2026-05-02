import types

import pytest

import puzzle_generator.bytestr_utils.bu_b16 as bu16
import puzzle_generator.bytestr_utils.bu_b32 as bu32
import puzzle_generator.bytestr_utils.bu_b32hex as bu32hex
import puzzle_generator.bytestr_utils.bu_b64 as bu64
import puzzle_generator.bytestr_utils.bu_b85 as bu85
import puzzle_generator.bytestr_utils.bu_standard_b64 as standard_bu64
import puzzle_generator.bytestr_utils.bu_urlsafe_b64 as urlsafe_bu64

from . import utils


def _get_encode_decode_pair(in_module: types.ModuleType):
    return in_module.bytes_to_bytestr, in_module.bytestr_to_bytes


@pytest.mark.parametrize(
    "in_bytes",
    utils.BYTES_LIST,
)
@pytest.mark.parametrize(
    "encode_decode_pair",
    [
        _get_encode_decode_pair(_)
        for _ in (bu16, bu32, bu32hex, bu64, bu85, standard_bu64, urlsafe_bu64)
    ],
)
def test_bytes_to_bytestr(in_bytes: bytes, encode_decode_pair) -> None:
    bytes_to_bytestr, bytestr_to_bytes = encode_decode_pair
    bytestr = bytes_to_bytestr(in_bytes)
    assert isinstance(bytestr, str)
    assert bytestr_to_bytes(bytestr) == in_bytes
