# heavily used functions
import curses
from Weapon import Weapon

stdscr = curses.initscr()
curses.start_color()
curses.use_default_colors()

# Allow the user to use a cursor to select between the given positions
# Returns the index of the position selected
def cursorOnPositions(positions, window):
    outfile = open("oot.txt",'w')
    positions = removeDupes(positions)
    selecting = True
    posit = 0
    y = positions[posit][0]
    x = positions[posit][1]
    while selecting:
        originalattrs = (window.inch(y,x) >> 8) & 0xFF
        outfile.write(str(originalattrs) + "\n")
        window.chgat(y,x,1,curses.color_pair(3))
        window.refresh()
        ch = stdscr.getch()
        if (ch == 10): # warning: may not work on all terminals/operating systems
            selecting = False
        elif (ch == curses.KEY_LEFT):
            if (posit-1 < 0):
                posit = len(positions)
            posit -= 1
        elif (ch == curses.KEY_RIGHT): # go right
            if (posit+1 == len(positions)):
                posit = -1
            posit += 1
        window.chgat(y,x,1,curses.color_pair(originalattrs))
        y = positions[posit][0]
        x = positions[posit][1]
    return posit

# Creates a new window, displays text centered around (y,x) and returns the window for potential usage
# Will make y,x the top left corner if specified
def textWindow(y,x,string, topLeft=False):
    halfwidth = -1
    halfheight = -1
    linestrings = []
    max = -1
    linestrings = string.split("\n")
    lines = string.count("\n") + 1
    max = ""
    for s in linestrings:
        if (len(s) + (s.count("\t")*7)) > len(max): # note that tabs = 7 spaces, for convenience
            max = s
    max = len(max) + (max.count("\t")*7)
    halfwidth = (max+4)/2
    halfheight = (len(linestrings)+4)/2
    if (topLeft):
        next = curses.newwin(4 + len(linestrings),4 + max,y,x)
    else:
        next = curses.newwin(4 + len(linestrings),4 + max, int(y-halfwidth),int(x-halfheight))
    next.box()
    pan = curses.panel.new_panel(next)
    for i in range(0,lines):
        next.addstr(i+2,2,linestrings[i])
    return (pan,next)

# write a "status bar" of a certain length, with the string
# returns it as a panel
def writeBar(y, x, length, string):
    win = curses.newwin(1,length+1,y,x)
    pan = curses.panel.new_panel(win)
    wStr = string + (" "*(length-len(string)))
    win.addstr(0,0,wStr,curses.color_pair(2))
    return [pan,win]

# returns true if pos[0],pos[1] is a valid space that can be walked on by a unit
def freespace(scenario,pos):
    if (pos[0] == len(scenario.rawmap)): return False # do this first so we don't crash on the next line
    row = scenario.rawmap[pos[0]]
    walls = scenario.wallchars
    return not(pos[1] == len(row) or pos[1] < 0 or pos[0] < 0) and walls.find(row[pos[1]]) == -1

# create the weapons dictionary by reading from weapons.list, return it
def readWeaponList(filename):
    outfile = open("outfile.txt",'w')
    file = open(filename,'r')
    lines = file.readlines()
    file.close()
    weaponlist = {"T":[],"S":[],"H":[],"L":[],"E":[],"N":[]}
    for line in lines:
        args = line.strip("\n").split("/")
        outfile.write(str(args) + "\n")
        w = Weapon(args[0],args[1],args[2],args[3],args[4])
        types = w.types
        for type in types:
            weaponlist[type].append(w)
    return weaponlist

# remove duplicate entries from a list
def removeDupes(l):
    seen = []
    for item in l:
        if item not in seen:
            seen.append(item)
    return seen


# determine if a point is within a polygon
# code taken from http://www.ariel.com.au/a/python-point-int-poly.html
def point_inside_polygon(x,y,poly):
    n = len(poly)
    inside =False
    p1x,p1y = poly[0]
    for i in range(n+1):
        p2x,p2y = poly[i % n]
        if y > min(p1y,p2y):
            if y <= max(p1y,p2y):
                if x <= max(p1x,p2x):
                    if p1y != p2y:
                        xinters = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x,p1y = p2x,p2y
    return inside
