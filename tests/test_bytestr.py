import pytest

import puzzle_generator.bytestr_utils as bu

from . import utils


@pytest.mark.parametrize(
    "in_bytes",
    utils.BYTES_LIST,
)
def test_bytes_to_bytestr(in_bytes: bytes) -> None:
    bytestr = bu.bytes_to_bytestr(in_bytes)
    assert isinstance(bytestr, str)
    assert bu.bytestr_to_bytes(bytestr) == in_bytes
