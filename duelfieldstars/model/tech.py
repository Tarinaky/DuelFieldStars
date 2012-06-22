"""
A file listing all technologies and providing special information in a
hopefully generic way.
"""
import math

class Technology(object):
    def __init__(self, name, max_level=None, check_special_func=None, advanced = False):
        self.name = name
        self.max_level = max_level
        self.check_special_func = check_special_func
        self.advanced = advanced

def is_square(i):
    if math.sqrt(float(i)) % 1 > 0:
        return False
    return True
    

a = [
                    Technology("Space Weapons Technology"),
                    Technology("Space Defence Technology"),
                    Technology("Ground Combat Technology"),
                    Technology("Production Technology"),
                    Technology("Growth Technology"),
                    Technology("Terraforming Technology"),
                    Technology("Mining Enhancement Technology", 100),
                    Technology("Colony Technology", 25, is_square),
                    Technology("Engine Technology")
                    
                    
                    ]

by_name = {} # Sort tech by name.
for technology in a:
    by_name[technology.name] = technology