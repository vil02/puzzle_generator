import pytest

from puzzle_generator.ea_configurators.eac_simple import eacs_simple
from puzzle_generator.ea_configurators.eac_simple import eacs_spiced


@pytest.mark.parametrize(
    "ea_configurator", [eacs_simple.EacsSimple, eacs_spiced.EacsSpiced]
)
def test_ea_configurators_raise_when_invalid_args(ea_configurator) -> None:
    with pytest.raises(TypeError):
        ea_configurator(wrong_param=10)
