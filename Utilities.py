# heavily used functions
import curses

stdscr = curses.initscr()
curses.start_color()
curses.use_default_colors()

# Allow the user to use a cursor to select between the given positions
# Returns the index of the position selected
def cursorOnPositions(positions, window):
    selecting = True
    posit = 0
    y = positions[posit][0]
    x = positions[posit][1]
    while selecting:
        oldchar = chr(window.inch(y,x) & 0xFF)
        window.addch(y,x,"X",curses.color_pair(1))
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
        window.addch(y,x,oldchar,curses.color_pair(4))
        y = positions[posit][0]
        x = positions[posit][1]
        window.refresh()
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
        if (len(s) + (s.count("\t")*5)) > len(max): # note that tabs = 5 spaces
            max = s
    max = len(max) + (max.count("\t")*5)
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
