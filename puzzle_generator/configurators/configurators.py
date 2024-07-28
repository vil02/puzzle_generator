from .simple import simple
from .simple import spiced


def get_configurator(**kwargs):
    encryption = kwargs.get("encryption", "spiced")
    configurators = {
        "simple": simple.Simple,
        "spiced": spiced.Spiced,
    }
    return configurators[encryption](**kwargs)
