import pytest

from puzzle_generator.encryption_algorithms.ea_simple import eas_common

from .. import utils


@pytest.mark.parametrize("in_signature_params", utils.SOME_SIGNATURE_PARAMS)
def test_digest_size(in_signature_params: dict[str, str]) -> None:
    some_hash = eas_common.sign_bytes(b"some_msg", b"some_key", in_signature_params)
    assert eas_common.digest_size(in_signature_params) == len(some_hash)


def test_split_data_and_signature_raises() -> None:
    with pytest.raises(ValueError, match="in_bytes is shorter than signature_size"):
        eas_common.split_data_and_signature(b"0", 2)
