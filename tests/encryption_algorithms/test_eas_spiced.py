import pytest

from puzzle_generator.encryption_algorithms.ea_simple import eas_spiced


def test_must_be_nonempty_raises() -> None:
    with pytest.raises(ValueError, match="in_list must be nonempty"):
        eas_spiced.must_be_nonempty([])
