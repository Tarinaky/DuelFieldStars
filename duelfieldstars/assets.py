"""
Obtain binary assets from a cache. Also includes a method to traverse and preload all assets.
"""

import os
import logging
import sys

log = logging.getLogger(__name__)

asset_path = "asset"
if not os.path.exists(asset_path):
    log(logging.DEBUG,"Could not find folder "+asset_path)
    sys.exit(1)

_cache = {} # A dictionary of assets sorted by a (type,filename) tuple.
_types = [] # A list of all types of assets.

def get(type_,filename):
    if (type_,filename) in _cache:
        return _cache[(type_,filename)]
    else:
        if type_().load(filename):
            return _cache[(type_,filename)]
        else:
            log(logging.DEBUG, "Could not find asset "+filename)
    
def preload():
    for type_ in _types:
        type_().load()