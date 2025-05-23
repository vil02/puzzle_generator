import typing

from .eas_common import (
    derive_key,
    digest_size,
    merge_data_and_signature,
    sign_bytes,
    split_data_and_signature,
    xor_bytes,
)


def get_encrypt(
    scrypt_params, signature_params
) -> typing.Callable[[bytes, bytes], bytes]:
    def _encrypt(in_bytes: bytes, in_pass: bytes) -> bytes:
        signature = sign_bytes(in_bytes, in_pass, signature_params)
        merged = merge_data_and_signature(in_bytes, signature)
        key = derive_key(password=in_pass, dklen=len(merged), **scrypt_params)
        return xor_bytes(merged, key)

    return _encrypt


def get_decrypt(
    scrypt_params, signature_params
) -> typing.Callable[[bytes, bytes], bytes | None]:
    def _decrypt(in_bytes: bytes, in_pass: bytes) -> bytes | None:
        key = derive_key(password=in_pass, dklen=len(in_bytes), **scrypt_params)
        data = xor_bytes(in_bytes, key)
        decrypted, signature = split_data_and_signature(
            data, digest_size(signature_params)
        )

        if sign_bytes(decrypted, in_pass, signature_params) == signature:
            return decrypted
        return None

    return _decrypt
