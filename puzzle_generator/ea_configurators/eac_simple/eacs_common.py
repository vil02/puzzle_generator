import secrets

from ... import bytes_utils as bu
from ... import bytestr_utils as bsu
from ... import puzzle_data_encryption as pde
from ...encryption_algorithms.simple import eas_common

MODULES = ["hmac", "hashlib", "base64", "sys", "typing"]

OBJECTS = [
    eas_common.sign_bytes,
    eas_common.derive_key,
    eas_common.split_data_and_signature,
    eas_common.digest_size,
    eas_common.xor_bytes,
    bsu.bytestr_to_bytes,
    bu.bytes_to_int,
    bu.split,
    pde.decrypt_data,
]


def scrypt_params(**kwargs):
    in_params = kwargs.get("scrypt_params", {})
    default = {"salt": secrets.token_bytes(16), "n": 2**14, "r": 8, "p": 1}
    if "maxmem" in in_params:
        default["maxmem"] = in_params["maxmem"]
    res = {_k: in_params.get(_k, _v) for _k, _v in default.items()}
    if "maxmem" not in res:
        res["maxmem"] = (128 + 100) * res["n"] * res["r"] * res["p"]
    return res


def signature_params(**kwargs):
    return kwargs.get("signature_params", {"digest": "sha512"})


def scrypt_params_to_code_str(**kwargs) -> str:
    pieces = [f'"{_k}":{_v}' for _k, _v in kwargs.items() if _k != "salt"]
    salt_str = '"' + bsu.bytes_to_bytestr(kwargs["salt"]) + '"'
    pieces.append(f'"salt":bytestr_to_bytes({salt_str})')
    return f"_SCRYPT_PARAMS = {{{','.join(pieces)}}}"
