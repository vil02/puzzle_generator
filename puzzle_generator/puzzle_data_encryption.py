import json


def encrypt_data(in_data, in_encrypt):
    if list(in_data.keys()) == ["str"]:
        return {"str": in_data["str"]}
    rest_str = json.dumps(encrypt_data(in_data["rest"], in_encrypt))
    encrypted_str = in_encrypt(rest_str, in_data["pass"])
    return {"str": in_data["str"], "rest": encrypted_str}


def decrypt_data(in_rest: str, in_pass: str, in_decrypt):
    rest_str = in_decrypt(in_rest, in_pass)
    if rest_str is None:
        return None
    return json.loads(rest_str)
