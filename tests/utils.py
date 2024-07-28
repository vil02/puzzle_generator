import puzzle_generator.encryption_algorithms.simple.simple as se
import puzzle_generator.encryption_algorithms.simple.spiced as sse


def get_simple_encrypt_decrypt_pair(*args):
    return se.get_encrypt(*args), se.get_decrypt(*args)


def get_spiced_simple_encrypt_decrypt_pair(*args):
    return sse.get_encrypt(*args), sse.get_decrypt(*args)
