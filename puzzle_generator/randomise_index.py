import secrets


def randomise_index(index: int, list_len: int, random_bits=128) -> int:
    if index < 0:
        raise ValueError("index must be non-negative")
    if index >= list_len:
        raise ValueError("index must be less than list_len")
    return secrets.randbits(random_bits) * list_len + index


def reduce_index(index: int, list_len: int) -> int:
    return index % list_len
