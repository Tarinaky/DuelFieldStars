"""
A file listing all technologies and providing special information in a
hopefully generic way.
"""
import math

class Technology(object):
    def __init__(self, name, desc, max_level=None, check_special_func=None, advanced = False):
        self.name = name
        self.desc = desc
        self.max_level = max_level
        self.check_special_func = check_special_func
        self.advanced = advanced

def is_square(i):
    if math.sqrt(float(i)) % 1 > 0:
        return False
    return True
    

a = [
                    Technology("Space Weapons Technology","Increases the Offensive Value of all ships."),
                    Technology("Space Defence Technology","Increases the Defensive Value of all ships."),
                    Technology("Ground Combat Technology","Increases the Combat Value of all ground forces."),
                    Technology("Production Technology","Increases the amount of Rez received from planetary Realisation."),
                    Technology("Growth Technology","Increases the amount of Realisation gained each turn."),
                    Technology("Terraforming Technology","Allows all worlds to slowly exceed their base value, increasing Rez income.",40),
                    Technology("Mining Enhancement Technology","Allows planets to unlock Mining Enhancements - increasing income by 1 rez each.", 100),
                    Technology("Colony Technology", "Allows a new type of world to be colonised at 4, 9, 16 and 25.",25, is_square),
                    Technology("Engine Technology", "Increases the speed and reaction of your ships.")
                    
                    
                    ]

by_name = {} # Sort tech by name.
for technology in a:
    by_name[technology.name] = technology