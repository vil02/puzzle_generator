from .eac_simple import eacs_simple, eacs_spiced


def get_ea_configurator(bu_configurator, **kwargs):
    encryption = kwargs.get("encryption", "spiced")
    configurators = {
        "simple": eacs_simple.EacsSimple,
        "spiced": eacs_spiced.EacsSpiced,
    }
    new_kwargs = {_k: _v for _k, _v in kwargs.items() if _k != "encryption"}
    return configurators[encryption](bu_configurator, **new_kwargs)
