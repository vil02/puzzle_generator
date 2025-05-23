import secrets
import typing

from .eas_common import (
    derive_key,
    digest_size,
    merge_data_and_signature,
    sign_bytes,
    split_data_and_signature,
    xor_bytes,
)


def must_be_nonempty(in_list: list[bytes]) -> None:
    if not in_list:
        raise ValueError("in_list must be nonempty")


def get_encrypt(
    proc_spices: list[bytes],
    signature_spices: list[bytes],
    scrypt_params,
    signature_params,
) -> typing.Callable[[bytes, bytes], bytes]:
    must_be_nonempty(proc_spices)
    must_be_nonempty(signature_spices)

    def _encrypt(in_bytes: bytes, in_pass: bytes) -> bytes:
        signature_spice = secrets.choice(signature_spices)
        signature = sign_bytes(in_bytes + signature_spice, in_pass, signature_params)
        merged = merge_data_and_signature(in_bytes, signature)
        proc_spice = secrets.choice(proc_spices)
        key = derive_key(
            password=in_pass + proc_spice, dklen=len(merged), **scrypt_params
        )
        return xor_bytes(merged, key)

    return _encrypt


def get_decrypt(
    proc_spices: list[bytes],
    signature_spices: list[bytes],
    scrypt_params,
    signature_params,
) -> typing.Callable[[bytes, bytes], bytes | None]:
    must_be_nonempty(proc_spices)
    must_be_nonempty(signature_spices)

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
                sign_bytes(decrypted + _, in_pass, signature_params) == signature
                for _ in signature_spices
            ):
                return decrypted
        return None

    return _decrypt
