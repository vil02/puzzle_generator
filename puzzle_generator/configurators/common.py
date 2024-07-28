import hashlib


def get_hasher_name(in_hasher) -> str:
    return "hashlib." + in_hasher().name


DefaultHasher = hashlib.sha512
