# WGM_api/__init__.py
from .wgm import WGM_api

def __call__(*args, **kwargs):
    return WGM_api(*args, **kwargs)