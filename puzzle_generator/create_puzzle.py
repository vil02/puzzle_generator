import importlib.metadata
import inspect
import typing

import black

from . import bu_configurators, rp_configurators
from .ea_configurators import ea_configurators
from .puzzle_data_creators import (
    hints_info,
    puzzle_description_to_sq_list,
    sq_list_to_dict,
)
from .puzzle_data_encryption import encrypt_data, encrypt_data_with_hints


def _advertisement() -> str:
    package_name = "puzzle-generator"
    full_name = f"{package_name} {importlib.metadata.version(package_name)}"
    return f"""# generated with {full_name}
#
# https://pypi.org/project/puzzle-generator/
# https://github.com/vil02/puzzle_generator/
"""


def _create_str(
    in_encrypted_puzzle: tuple[str, bytes] | tuple[str, int, bytes],
    ea_configurator,
    rp_configurator,
) -> str:
    modules: str = (
        "\n".join("import " + _ for _ in ea_configurator.get_modules()) + "\n"
    )
    objects: str = "\n".join(
        inspect.getsource(_)
        for _ in ea_configurator.get_needed_objects()
        + rp_configurator.get_needed_objects()
    )

    return (
        "\n".join(
            [
                _advertisement(),
                modules,
                'BYTEORDER: typing.Literal["little", "big"] = "little"',
                objects,
                rp_configurator.puzzle_data(
                    in_encrypted_puzzle,
                    ea_configurator.bu_configurator.bytes_to_bytestr(),
                ),
                ea_configurator.get_constants_str(),
                rp_configurator.call(),
            ]
        )
        + "\n"
    )


def encrypt_puzzle(
    sq_list: typing.Sequence[tuple[str, str, typing.Callable[[str], str] | None]],
    final_str: str,
    hint_to_index: dict[typing.Callable[[str], str] | None, int] | None,
    in_encrypt: typing.Callable[[bytes, bytes], bytes],
) -> tuple[str, bytes] | tuple[str, int, bytes]:
    puzzle = sq_list_to_dict(sq_list, final_str, hint_to_index)
    if hint_to_index is None:
        return encrypt_data(puzzle, in_encrypt)
    return encrypt_data_with_hints(puzzle, in_encrypt)


def create(
    puzzle_description: (
        list[str]
        | typing.Sequence[tuple[str, str, typing.Callable[[str], str] | None] | str]
    ),
    **kwargs,
) -> str:
    sq_list, final_str = puzzle_description_to_sq_list(puzzle_description)
    unique_hints, hint_to_index = hints_info(sq_list)

    ea_configurator = ea_configurators.get_ea_configurator(
        bu_configurators.get_bu_configurator(kwargs.get("encoding", "base64")),
        **{_k: _v for _k, _v in kwargs.items() if _k != "encoding"},
    )

    encrypted_puzzle = encrypt_puzzle(
        sq_list, final_str, hint_to_index, ea_configurator.get_encrypt()
    )
    res = _create_str(
        encrypted_puzzle,
        ea_configurator,
        rp_configurators.get_rp_configurator(unique_hints),
    )
    return black.format_str(res, mode=black.FileMode())
