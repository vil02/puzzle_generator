import re

import pytest

from puzzle_generator import bu_configurators as buc
from puzzle_generator.ea_configurators.eac_simple import eacs_simple, eacs_spiced


@pytest.mark.parametrize(
    "ea_configurator", [eacs_simple.EacsSimple, eacs_spiced.EacsSpiced]
)
@pytest.mark.parametrize(
    "bu_configurator",
    [buc.get_bu_configurator("base64"), buc.get_bu_configurator("base85")],
)
def test_ea_configurators_raise_when_invalid_args(
    ea_configurator, bu_configurator
) -> None:
    with pytest.raises(
        TypeError, match=re.escape("wrong_param is an invalid keyword argument")
    ):
        ea_configurator(bu_configurator, wrong_param=10)
