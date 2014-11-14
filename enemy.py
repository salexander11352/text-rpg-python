
class Enemy(object):

    '''
    Class Attributes:
        name: goblin, skeleton, etc
        desc: description of creature
        attr: dict of stats 
        hp:   hp of creature
        gear: dict of equipment stats
        pos:  0, X Coord; 1, Y Coord
    '''
    
    def __init__(self, x, y):
        self.pos = [x, y]
        self.hp  = self._calcHP(self.attr["vit"])

    def _calcHP(vit): # Private?
        return (vit * 65)

    def damage(self, amount):
        self.hp -= amount;

    def heal(self, amount):
        self.hp += amount;

class Goblin(Enemy):

    def __init__(self, x, y): 
        self.name = "Goblin"
        self.desc = ("A generic goblin. A grotesque little green humanoid "
                     "with crooked teeth, pointy ears, and a general lack "
                     "of civility.")
        self.attr = { "vit" : 10,
                      "int" :  5,
                      "end" :  5,
                      "str" : 10,
                      "dex" : 10,
                      "mag" :  5,
                      "fth" :  5,
                      "lck" :  9 }
        self.gear = { "wpn" :  0,
                      "arm" :  0 }
        super(Goblin, self).__init__(x, y)

