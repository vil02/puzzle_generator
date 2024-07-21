import pytest

import puzzle_generator.bytestr_utils as bu


@pytest.mark.parametrize(
    "in_bytes",
    [
        "".encode(),
        "some_str".encode(),
        "ąĘćŚłŁÓ".encode(),
        "🐍".encode(),
        "👍😄💾".encode(),
        b"\0",
        b"1235",
    ],
)
def test_bytes_to_bytestr(in_bytes):
    bytestr = bu.bytes_to_bytestr(in_bytes)
    assert isinstance(bytestr, str)
    assert bu.bytestr_to_bytes(bytestr) == in_bytes
