import hashlib
import hmac


def digest_size(params) -> int:
    hasher = hashlib.new(params["digest"])
    return hasher.digest_size


def sign_bytes(in_bytes: bytes, in_key: bytes, params) -> bytes:
    return hmac.digest(msg=in_bytes, key=in_key, **params)


def derive_key(**kwargs) -> bytes:
    return hashlib.scrypt(**kwargs)


def xor_bytes(in_bytes: bytes, in_key: bytes) -> bytes:
    """xors the in_bytes with a sequence of bytes with in_key"""
    return bytes(_d ^ _k for (_d, _k) in zip(in_bytes, in_key, strict=True))


def merge_data_and_signature(in_data: bytes, in_signature: bytes) -> bytes:
    return in_data + in_signature


def split_data_and_signature(
    in_bytes: bytes, signature_size: int
) -> tuple[bytes, bytes]:
    if len(in_bytes) < signature_size:
        raise ValueError("in_bytes is shorter than signature_size")
    data = in_bytes[:-signature_size]
    signature = in_bytes[-signature_size:]
    return data, signature
