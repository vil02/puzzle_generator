import typing

from . import bytes_utils as bu
from . import puzzle_data_encryption as pde
from . import randomise_index as ri
from . import run_puzzle as rp
from . import string_to_code


class _NoHintsConfigurator:
    def get_needed_objects(self):
        return [bu.split_bytes_blocks, bu.split, pde.decrypt_data, rp.run_puzzle]

    def puzzle_data(
        self, in_encrypted_puzzle: tuple[str, bytes], bytes_to_bytestr
    ) -> str:
        question = string_to_code.string_to_code(in_encrypted_puzzle[0], 78, '"""')
        rest_str = string_to_code.string_to_code(
            bytes_to_bytestr(in_encrypted_puzzle[1]),
            78,
            '"',
        )
        return f"_PUZZLE = ({question}, bytestr_to_bytes({rest_str}))"

    def call(self) -> str:
        return "run_puzzle(_PUZZLE, _DECRYPT, input)"


def _get_name(in_fun: typing.Callable[[str], str] | None) -> str:
    if in_fun is None:
        return "None"
    return in_fun.__name__


class _WithHintsConfigurator:
    def __init__(self, in_unique_hints: list[typing.Callable[[str], str] | None]):
        self.unique_hints = in_unique_hints

    def get_needed_objects(self):
        return [
            bu.split_bytes_blocks,
            bu.split,
            bu.split_with_hints,
            pde.decrypt_data_with_hints,
            ri.reduce_index,
            rp.run_puzzle_with_hints,
        ] + [_ for _ in self.unique_hints if _ is not None]

    def puzzle_data(
        self, in_encrypted_puzzle: tuple[str, int, bytes], bytes_to_bytestr
    ) -> str:
        question = string_to_code.string_to_code(in_encrypted_puzzle[0], 78, '"""')
        hint_index = in_encrypted_puzzle[1] % len(self.unique_hints)
        rest_str = string_to_code.string_to_code(
            bytes_to_bytestr(in_encrypted_puzzle[2]),
            78,
            '"',
        )
        hints_str = ", ".join(_get_name(_) for _ in self.unique_hints)
        hints = f"[{hints_str}]"
        return (
            f"_HINTS = {hints}\n"
            f"_PUZZLE = ({question}, {hint_index}, bytestr_to_bytes({rest_str}))"
        )

    def call(self) -> str:
        return "run_puzzle_with_hints(_PUZZLE, _HINTS, _DECRYPT, input)"


def get_rp_configurator(unique_hints: list[None | typing.Callable[[str], str]] | None):
    if unique_hints is None:
        return _NoHintsConfigurator()
    return _WithHintsConfigurator(unique_hints)
