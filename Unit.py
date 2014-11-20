# contains the class representing a unit

class Unit:
    

    def __init__(self,name,type,hp,att,pos,friendly):
        self.name = name
        self.type = type
        self.hp = hp
        self.att = att
        self.pos = pos
        self.friendly = friendly

    # Things that need doing here:
    # AI methods
    # getAttack/takeDamage
