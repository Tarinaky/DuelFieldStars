"""
Obtain binary assets from a cache. Also includes a method to traverse and preload all assets.
"""

__all__ = ['PNG']

import os
import logging
import sys

log = logging.getLogger(__name__)

asset_path = "asset"

_cache = {} # A dictionary of assets sorted by a (type,filename) tuple.
_types = [] # A list of all types of asset

def get(type_,filename):
    if (type_,filename) in _cache:
        return _cache[(type_,filename)]
    else:
        if type_().load(filename):
            return _cache[(type_,filename)]
        else:
            log.debug("Could not find asset "+filename)
    
def preload(): # FIXME: Not tested, may not work.
    for type_ in _types:
        type_().load()
        
class Type(object):
    """
    An abstract class representing a type of binary asset that can be loaded.
    """
    def load(self,filename=None): # return True
        """Overload this. Load the specified filename into the cache.
        If filename is None instead load all assets from the directory structure. Must return True"""
        pass
    
