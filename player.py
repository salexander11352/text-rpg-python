import random

class Player(object):
    
    '''
    Class Attributes:

        Implemented:
            name: Character name
            hp:
            attr: dict of player stats
            gear: dict of equip stats
            pos:  0, XCoord;; 1, YCoord

        Not yet Implemented:
            inventory: Waiting on a stable item system

    '''
    
    spawnLoc = [[5, 7], [5, 20], [21, 21]]
    pos      = [-1, -1]

    def __init__(self, n, a, g):
        self.name = n
        self.attr = a
        self.gear = g
        self.hp   = ( self.attr["vit"] * ( 50 + ( self.attr["vit"] * 4.5 )))

    def spawnCoords(self, x, y):
        self.pos  = [x, y]

    def spawnRandom(self):
        randSpawn = random.randint(1,len(self.spawnLoc)) - 1
        self.pos = self.spawnLoc[randSpawn]

    def damage(self, amount):
        self.hp -= amount

    def heal(self, amount):
        self.hp += amount

