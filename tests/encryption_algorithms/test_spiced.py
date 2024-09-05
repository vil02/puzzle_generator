import pytest

import puzzle_generator.encryption_algorithms.simple.spiced as ess


def test_must_be_nonempty_raises() -> None:
    with pytest.raises(ValueError, match="in_list must be nonempty"):
        ess.must_be_nonempty([])
