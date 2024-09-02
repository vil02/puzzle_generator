import itertools

import pytest

import puzzle_generator.bytes_utils as bu
from . import utils


@pytest.mark.parametrize(
    ("in_value", "expected"),
    [
        (0, 0),
        (1, 1),
        (2, 1),
        (3, 1),
        (255, 1),
        (256, 2),
        (257, 2),
        (2 ** (8 * 255) - 1, 255),
        (2 ** (8 * 255), 256),
    ],
)
def test_byte_length(in_value: int, expected: int) -> None:
    assert bu.byte_length(in_value) == expected


def test_byte_length_raises_for_negative_input() -> None:
    with pytest.raises(ValueError, match="in_value must be non-negative"):
        bu.byte_length(-1)


@pytest.mark.parametrize(
    "in_value", [0, 1, 2, 3, 255, 256, 257, 3239949409384, 10**570, 2 ** (8 * 255) - 1]
)
def test_int_to_bytes(in_value: int) -> None:
    assert bu.bytes_to_int(bu.int_to_bytes(in_value)) == in_value


def test_bytes_to_int_raises_when_input_has_wrong_length():
    with pytest.raises(ValueError, match="in_bytes has wrong structure"):
        bu.bytes_to_int(bytes([2, 1]))


def test_int_to_bytes_raises_when_input_is_too_big() -> None:
    with pytest.raises(ValueError, match="in_value must be 255 bytes or less"):
        bu.int_to_bytes(2 ** (8 * 255))


@pytest.mark.parametrize(
    ("in_str", "in_bytes"), itertools.product(utils.STRS, utils.BYTES_LIST)
)
def test_split_and_join(in_str: str, in_bytes: bytes) -> None:
    res_str, res_bytes = bu.split(bu.join(in_str, in_bytes))
    assert res_str == in_str
    assert res_bytes == in_bytes
