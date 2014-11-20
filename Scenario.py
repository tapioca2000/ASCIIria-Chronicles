# Scenario class - stores all information about the scenario

from Unit import Unit
import curses

curses.initscr()
class Scenario:

    # Read text file, generate list of enemy units, organize tile data, generate map pad
    def __init__(self,filename):
        curses.start_color()
        curses.use_default_colors()
        file = open(filename,'r')
        out = open("out.txt",'w')
        lines = file.readlines()
        enemycount = int(lines[0])
        c = 1
        self.units = []
        for x in range(1,enemycount+1):
            attrs = lines[x].strip("\n").split("/")
            pos = [attrs[5],attrs[4]] # x,y in the text file but y,x in the code (for ease of creation)
            self.units.append(Unit(attrs[0],attrs[1],attrs[2],attrs[3],pos,False))
            c += 1
        maplength = int(lines[c])
        self.map = curses.newpad(maplength,maplength + 1)
        self.mapcolors = []
        for x in range(c+1,c+maplength+1):
            self.mapcolors.append(lines[x].strip("\n")[1:len(lines[x]):2])
            col = 0
            out.write(lines[x].strip("\n")[0:len(lines[x]):2] + "\n")
            for ch in lines[x].strip("\n")[0:len(lines[x]):2]:
                out.write(str(x-(c+1)) + " " + str(col) + " " + ch + " " + self.mapcolors[x-(c+1)][col] + "\n")
                self.map.addch(x-(c+1),col,ch,curses.color_pair(int(self.mapcolors[x-(c+1)][col])))
                col += 1
