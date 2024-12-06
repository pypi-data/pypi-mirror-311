from .wgm import WGM_api as _WGM_api

def __new__(*args, **kwargs):
    return _WGM_api(*args, **kwargs)

WGM_api = _WGM_api