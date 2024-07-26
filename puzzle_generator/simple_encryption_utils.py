import itertools
import typing


def hash_bytes(in_bytes: bytes, in_hasher) -> bytes:
    return in_hasher(in_bytes).digest()


def int_to_bytes(in_val: int) -> bytes:
    return in_val.to_bytes((in_val.bit_length() + 7) // 8, "big")


def proc_bytes(in_bytes: bytes, in_key: bytes, in_hasher) -> bytes:
    """xors the in_bytes with a sequence of bytes generated with in_key"""
    key_bytes = itertools.chain.from_iterable(
        in_hasher(in_key + int_to_bytes(block_num)).digest()
        for block_num in itertools.count(0)
    )
    return bytes(_d ^ _k for (_d, _k) in zip(in_bytes, key_bytes))


def merge_encrypted_and_signature(in_encrypted: bytes, in_signature: bytes) -> bytes:
    return in_encrypted + in_signature


def split_encrypted_and_signature(
    in_bytes: bytes, signature_size: int
) -> typing.Tuple[bytes, bytes]:
    assert len(in_bytes) >= signature_size
    encrypted = in_bytes[:-signature_size]
    signature = in_bytes[-signature_size:]
    return encrypted, signature
