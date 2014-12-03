# contains the class representing a unit

import random

unitweaknesses = {"T":"L","S":"HN","H":"LN","L":"TN","E":"TSHLN","N":"TSHL"} # unit weaknesses

class Unit:
    

    def __init__(self,name,type,hp,att,pos,friendly):
        self.name = name
        self.type = type
        self.hp = hp
        self.att = att
        self.pos = pos
        self.friendly = friendly

    # movement (assume that the space to be moved to is free)
    def move_left(self):
        self.pos[1] -= 1
    def move_right(self):
        self.pos[1] += 1
    def move_up(self):
        self.pos[0] -= 1
    def move_down(self):
        self.pos[0] += 1

    # unit has been targeted for attack, calculate and take damage
    def attacked(acc,att,type):
        if (randint(0,100) <= (acc*100)): # damage will be done
            dmg = randint(att-5,att+5)
            if unitweaknesses[self.type].find(type) >= 0: # this unit is weak to the enenmy unit type
                dmg += 3
            self.hp -= dmg
