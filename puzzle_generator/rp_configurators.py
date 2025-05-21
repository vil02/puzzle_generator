import typing

from . import run_puzzle as rp


class _NoHintsConfigurator:
    def get_needed_objects(self):
        return [rp.run_puzzle]

    def puzzle_data(self, question: str, rest_str: str) -> str:
        return f"_PUZZLE = ({question}, bytestr_to_bytes({rest_str}))"

    def call(self) -> str:
        return "run_puzzle(_PUZZLE, _DECRYPT, input)"


def get_proc_answer(
    in_hints: typing.Sequence[typing.Callable[[str], str] | None],
) -> typing.Callable[[str], str]:
    cur_answer = 0

    def _proc_answer(in_str: str) -> str:
        nonlocal cur_answer
        res = in_str
        cur_hint = in_hints[cur_answer]
        cur_answer += 1
        if cur_hint is not None:
            res = cur_hint(res)
        return res

    return _proc_answer


def _get_name(in_fun: typing.Callable[[str], str] | None) -> str:
    if in_fun is None:
        return "None"
    return in_fun.__name__


class _WithHintsConfigurator:
    def __init__(self, in_hints: list[typing.Callable[[str], str] | None]):
        self.hints = in_hints

    def get_needed_objects(self):
        res = [get_proc_answer, rp.run_puzzle, rp.run_puzzle_with_hints]
        for _ in set(self.hints):
            if _ is not None:
                res.append(_)
        return res

    def puzzle_data(self, question: str, rest_str: str) -> str:
        hints_str = ", ".join(_get_name(_) for _ in self.hints)
        hints = f"[{hints_str}]"
        res_a = f"_HINTS = {hints}"
        res_b = f"_PUZZLE = ({question}, bytestr_to_bytes({rest_str}))"
        return "\n".join((res_a, res_b))

    def call(self) -> str:
        return (
            "run_puzzle_with_hints(_PUZZLE, _DECRYPT, input, get_proc_answer(_HINTS))"
        )


def get_rp_configurator(hints: list[None | typing.Callable[[str], str]]):
    if all(_ is None for _ in hints):
        return _NoHintsConfigurator()
    return _WithHintsConfigurator(hints)
