import secrets

from ... import bytestr_utils as bu

MODULES = ["hashlib", "base64", "sys", "typing"]


def scrypt_params(**kwargs):
    print(kwargs)
    default = {"salt": secrets.token_bytes(16), "n": 2**14, "r": 8, "p": 1}
    if "maxmem" in kwargs:
        default["maxmem"] = kwargs["maxmem"]
    res = {_k: kwargs.get(_k, _v) for _k, _v in default.items()}
    if "maxmem" not in res:
        res["maxmem"] = (128 + 100) * res["n"] * res["r"] * res["p"]
    return res


def scrypt_params_to_code_str(**kwargs) -> str:
    pieces = [f'"{_k}":{_v}' for _k, _v in kwargs.items() if _k != "salt"]
    salt_str = '"' + bu.bytes_to_bytestr(kwargs["salt"]) + '"'
    pieces.append(f'"salt":bytestr_to_bytes({salt_str})')
    return f"_SCRYPT_PARAMS = {{{','.join(pieces)}}}"
