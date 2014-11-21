# Scenario class - stores all information about the map and what's on it
# handles basically everything relating to the map and its current state

from Unit import Unit
import curses

curses.initscr()
class Scenario:

    # Read text file, generate list of enemy units, organize tile data, generate map pad
    def __init__(self,filename):
        curses.start_color()
        curses.use_default_colors()
        file = open(filename,'r')
        lines = file.readlines()
        enemycount = int(lines[0])
        c = 1
        self.units = []
        for x in range(1,enemycount+1):
            attrs = lines[x].strip("\n").split("/")
            pos = [int(attrs[5]),int(attrs[4])] # x,y in the text file but y,x in the code (for ease of creation)
            self.units.append(Unit(attrs[0],attrs[1],attrs[2],attrs[3],pos,False))
            c += 1
        maplength = int(lines[c])
        self.map = curses.newpad(maplength,maplength + 1) # map in its current state at any point
        self.maplines = [] # raw map
        self.mapcolors = []
        self.openings = []
        for x in range(c+1,c+maplength+1):
            self.maplines.append(lines[x].strip("\n")[0:len(lines[x]):2])
            self.mapcolors.append(lines[x].strip("\n")[1:len(lines[x]):2])
            col = 0
            for ch in lines[x].strip("\n")[0:len(lines[x]):2]:
                if (ch == 'O'):
                    pairnumber = 4 # all open spots are blue
                    self.openings.append([x-(c+1), col])
                else:
                    pairnumber = int(self.mapcolors[x-(c+1)][col]) # use given color
                self.map.addch(x-(c+1),col,ch,curses.color_pair(pairnumber))
                col += 1
        for unit in self.units:
            posit = unit.pos
            self.map.addch(posit[1],posit[0],unit.type,curses.color_pair(1)) # red because Imperals
