from .simple import simple
from .simple import spiced


def get_configurator(**kwargs):
    encryption = kwargs.get("encryption", "spiced")
    configurators = {
        "simple": simple.Simple,
        "spiced": spiced.Spiced,
    }
    new_kwargs = {_k: _v for _k, _v in kwargs.items() if _k != "encryption"}
    return configurators[encryption](**new_kwargs)
