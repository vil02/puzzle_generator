import json
import typing


def encrypt_data(in_data, in_encrypt: typing.Callable[[str, str], str]):
    if list(in_data.keys()) == ["str"]:
        return {"str": in_data["str"]}
    rest: str = json.dumps(encrypt_data(in_data["rest"], in_encrypt))
    encrypted: str = in_encrypt(rest, in_data["pass"])
    return {"str": in_data["str"], "rest": encrypted}


def decrypt_data(
    in_rest: str, in_pass: str, in_decrypt: typing.Callable[[str, str], str | None]
):
    rest_str = in_decrypt(in_rest, in_pass)
    if rest_str is None:
        return None
    return json.loads(rest_str)
