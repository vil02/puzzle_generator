import itertools

import pytest

import puzzle_generator.bytes_utils as bu
from . import utils


@pytest.mark.parametrize(
    "in_value", [0, 1, 2, 3, 255, 256, 257, 3239949409384, 10**570]
)
def test_int_to_bytes(in_value):
    assert bu.bytes_to_int(bu.int_to_bytes(in_value)) == in_value


@pytest.mark.parametrize(
    ("in_str", "in_bytes"), itertools.product(utils.STRS, utils.BYTES_LIST)
)
def test_split_and_join(in_str, in_bytes):
    res_str, res_bytes = bu.split(bu.join(in_str, in_bytes))
    assert res_str == in_str
    assert res_bytes == in_bytes
