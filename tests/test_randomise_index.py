import pytest

import puzzle_generator._randomise_index as ri


@pytest.mark.parametrize(
    ("index", "list_len"),
    [
        (0, 5),
        (1, 2),
        (0, 1),
        (992142, 3454333),
    ],
)
def test_randomise_index(index: int, list_len: int) -> None:
    assert ri.reduce_index(ri.randomise_index(index, list_len), list_len) == index


def test_randomise_index_raises_for_negative_input() -> None:
    with pytest.raises(ValueError, match="index must be non-negative"):
        ri.randomise_index(-1, 10)


def test_randomise_index_raises_for_large_input() -> None:
    with pytest.raises(ValueError, match="index must be less than list_len"):
        ri.randomise_index(10, 10)
