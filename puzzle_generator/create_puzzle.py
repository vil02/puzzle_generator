import inspect

from .puzzle_data_encryption import encrypt_data
from .configurators import configurators


def _create_str(in_modules, in_objects, in_encrypted_puzzle, constants: str) -> str:
    advertisement = """# generated with puzzle-generator
#
# https://pypi.org/project/puzzle-generator/
# https://github.com/vil02/puzzle_generator/
"""
    modules: str = "\n".join("import " + _ for _ in in_modules) + "\n"
    objects: str = "\n".join(inspect.getsource(_) for _ in in_objects)
    puzzle_data: str = f"_PUZZLE = {in_encrypted_puzzle}"
    call: str = "run_puzzle(_PUZZLE, _DECRYPT, input)"

    return (
        "\n".join(
            [
                advertisement,
                modules,
                objects,
                puzzle_data,
                constants,
                call,
            ]
        )
        + "\n"
    )


def create(in_puzzle, **kwargs) -> str:
    configurator = configurators.get_configurator(**kwargs)

    encrypted_puzzle = encrypt_data(in_puzzle, configurator.get_encrypt())
    needed_modules = ["hashlib", "itertools", "base64", "json", "sys", "typing"]

    needed_objects = configurator.get_needed_objects()
    constants: str = configurator.get_constants_str()

    return _create_str(needed_modules, needed_objects, encrypted_puzzle, constants)
