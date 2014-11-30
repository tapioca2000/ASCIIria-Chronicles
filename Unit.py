# contains the class representing a unit

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
