import pytest

import puzzle_generator.encryption_algorithms.simple.common as eac
from .. import utils


@pytest.mark.parametrize("in_hash_params", utils.SOME_SIGNATURE_PARAMS)
def test_digest_size(in_hash_params):
    some_hash = eac.hash_bytes(b"some_msg", in_hash_params)
    assert eac.digest_size(in_hash_params) == len(some_hash)
