import hashlib
import typing


def digest_size(params) -> int:
    hasher = hashlib.new(**params["hasher"])
    res = hasher.digest_size
    if res > 0:
        return res
    return params["digest"]["length"]


def hash_bytes(in_bytes: bytes, params) -> bytes:
    hasher = hashlib.new(**params["hasher"])
    hasher.update(in_bytes)
    res = hasher.digest(**params["digest"])
    return res


def derive_key(**kwargs):
    return hashlib.scrypt(**kwargs)


def xor_bytes(in_bytes: bytes, in_key: bytes) -> bytes:
    """xors the in_bytes with a sequence of bytes with in_key"""
    return bytes(_d ^ _k for (_d, _k) in zip(in_bytes, in_key, strict=True))


def merge_data_and_signature(in_data: bytes, in_signature: bytes) -> bytes:
    return in_data + in_signature


def split_data_and_signature(
    in_bytes: bytes, signature_size: int
) -> typing.Tuple[bytes, bytes]:
    assert len(in_bytes) >= signature_size  # nosec B101
    data = in_bytes[:-signature_size]
    signature = in_bytes[-signature_size:]
    return data, signature
