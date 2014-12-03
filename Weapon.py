# basic weapon class

class Weapon:
    def __init__(self,name,types,range,att,acc):
        self.name = name
        self.types = list(types)
        self.range = int(range)
        self.att = int(att)
        self.acc = float(acc)
