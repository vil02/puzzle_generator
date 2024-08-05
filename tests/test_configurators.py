import pytest

from puzzle_generator.configurators.simple import simple
from puzzle_generator.configurators.simple import spiced


@pytest.mark.parametrize("configurator", [simple.Simple, spiced.Spiced])
def test_configurators_raise_when_invalid_args(configurator):
    with pytest.raises(TypeError):
        configurator(wrong_param=10)
