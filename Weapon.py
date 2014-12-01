# basic weapon class

class Weapon:
    def __init__(self,name,types,range,att,acc):
        self.name = name
        self.types = list(types)
        self.range = range
        self.att = att
        self.acc = acc
