# Scenario class - stores all information about the map and what's on it
# handles basically everything relating to the map and its current state

from Unit import Unit
import curses

curses.initscr()
class Scenario:

    # Read text file, generate list of enemy units, organize tile data, generate map pad
    def __init__(self,filename,mapy,mapx):
        self.mapy = mapy
        self.mapx = mapx
        curses.start_color()
        curses.use_default_colors()
        file = open(filename,'r')
        lines = file.readlines()
        enemycount = int(lines[0])
        c = 1
        self.enemyunits = []
        self.friendlyunits = []
        self.rawmap = []
        for x in range(1,enemycount+1): # Create enemy units
            attrs = lines[x].strip("\n").split("/")
            pos = [int(attrs[4]),int(attrs[5])]
            self.enemyunits.append(Unit(attrs[0],attrs[1],attrs[2],attrs[3],pos,False))
            c += 1
        maplength = int(lines[c])
        self.maplength = maplength
        self.map = curses.newwin(maplength,maplength + 1) # map, without any units
        self.mapcolors = []
        self.openings = []
        for x in range(c+1,c+maplength+1): # create rawmap, mapcolors
            self.rawmap.append(lines[x].strip("\n")[0:len(lines[x]):2])
            self.mapcolors.append(lines[x].strip("\n")[1:len(lines[x]):2])
            col = 0
            for ch in lines[x].strip("\n")[0:len(lines[x]):2]: # initial map setup
                if (ch == ' '):
                    pairnumber = 4 # all open spots are blue
                    self.openings.append([x-(c+1), col])
                else:
                    pairnumber = int(self.mapcolors[x-(c+1)][col]) # use given color
                self.map.addch(x-(c+1),col,ch,curses.color_pair(pairnumber))
                col += 1

    # add unit to units list, update map
    def addUnit(self,unit):
        outfile = file("outfile.txt",'w')
        outfile.write("Adding " + unit.name + " to the unit lists\n")
        if (unit.friendly):
            self.friendlyunits.append(unit)
        else:
            self.enemyunits.append(unit)

    # update window the panel is based on
    def updateMap(self):
        out = open("outfilee.txt",'w')
        self.map = curses.newwin(self.maplength,self.maplength+1, self.mapy, self.mapx)
        for x in range(0,len(self.rawmap)):
            col = 0
            for ch in self.rawmap[x]:
                color = int(self.mapcolors[x][col])
                self.map.addch(x,col,ch,curses.color_pair(color))
                col += 1
        for unit in self.friendlyunits:
            out.write("Adding " + unit.name + " to board at " + str(unit.pos) + "\n")
            self.map.addch(unit.pos[0],unit.pos[1],unit.type,curses.color_pair(4))
        for unit in self.enemyunits:
            self.map.addch(unit.pos[0],unit.pos[1],unit.type,curses.color_pair(1))

    # return map panely
    def mapPan(self):
        pan = curses.panel.new_panel(self.map)
        pan.move(self.mapy,self.mapx)
        return pan
