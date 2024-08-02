import typing
import secrets

from .common import (
    derive_key,
    xor_bytes,
    hash_bytes,
    digest_size,
    merge_data_and_signature,
    split_data_and_signature,
)


def get_encrypt(
    proc_spices: typing.List[bytes],
    signature_spices: typing.List[bytes],
    scrypt_params,
    signature_params,
) -> typing.Callable[[bytes, bytes], bytes]:
    assert proc_spices  # nosec B101
    assert signature_spices  # nosec B101

    def _encrypt(in_bytes: bytes, in_pass: bytes) -> bytes:
        signature_spice = secrets.choice(signature_spices)
        signature = hash_bytes(in_bytes + signature_spice, signature_params)
        merged = merge_data_and_signature(in_bytes, signature)
        proc_spice = secrets.choice(proc_spices)
        key = derive_key(
            password=in_pass + proc_spice, dklen=len(merged), **scrypt_params
        )
        return xor_bytes(merged, key)

    return _encrypt


def get_decrypt(
    proc_spices: typing.List[bytes],
    signature_spices: typing.List[bytes],
    scrypt_params,
    signature_params,
) -> typing.Callable[[bytes, bytes], bytes | None]:
    assert proc_spices  # nosec B101
    assert signature_spices  # nosec B101

    def _decrypt(in_bytes: bytes, in_pass: bytes) -> bytes | None:
        for proc_spice in proc_spices:
            key = derive_key(
                password=in_pass + proc_spice, dklen=len(in_bytes), **scrypt_params
            )
            data = xor_bytes(in_bytes, key)
            decrypted, signature = split_data_and_signature(
                data, digest_size(signature_params)
            )

            if any(
                hash_bytes(decrypted + _, signature_params) == signature
                for _ in signature_spices
            ):
                return decrypted
        return None

    return _decrypt
