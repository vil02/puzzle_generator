import typing


from .common import (
    derive_key,
    xor_bytes,
    hash_bytes,
    digest_size,
    merge_data_and_signature,
    split_data_and_signature,
)


def get_encrypt(
    scrypt_params, signature_params
) -> typing.Callable[[bytes, bytes], bytes]:
    def _encrypt(in_bytes: bytes, in_pass: bytes) -> bytes:
        signature = hash_bytes(in_bytes, signature_params)
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

        if hash_bytes(decrypted, signature_params) == signature:
            return decrypted
        return None

    return _decrypt
