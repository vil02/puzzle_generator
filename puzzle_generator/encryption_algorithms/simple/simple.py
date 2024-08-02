import typing


from .common import (
    derive_key,
    xor_bytes,
    hash_bytes,
    merge_data_and_signature,
    split_data_and_signature,
)


def get_encrypt(
    signature_hasher, scrypt_params
) -> typing.Callable[[bytes, bytes], bytes]:
    def _encrypt(in_bytes: bytes, in_pass: bytes) -> bytes:
        signature = hash_bytes(in_bytes, signature_hasher)
        merged = merge_data_and_signature(in_bytes, signature)
        key = derive_key(password=in_pass, dklen=len(merged), **scrypt_params)
        return xor_bytes(merged, key)

    return _encrypt


def get_decrypt(
    signature_hasher, scrypt_params
) -> typing.Callable[[bytes, bytes], bytes | None]:
    def _decrypt(in_bytes: bytes, in_pass: bytes) -> bytes | None:
        key = derive_key(password=in_pass, dklen=len(in_bytes), **scrypt_params)
        data = xor_bytes(in_bytes, key)
        decrypted, signature = split_data_and_signature(
            data, signature_hasher().digest_size
        )

        if hash_bytes(decrypted, signature_hasher) == signature:
            return decrypted
        return None

    return _decrypt
