# ASCIIria Chronicles

# nbsp: 

import curses, time
from curses import wrapper, panel
stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
stdscr.keypad(True)
curses.curs_set(0)
pad = curses.newpad(curses.LINES,curses.COLS) # field

# draw the borders around the screen, fancily
def drawBorders():
    horizBorder = '*' * (curses.COLS)
    pad.addstr(0,0,horizBorder)
    for y in range(1,curses.LINES-1):
        pad.refresh(0,0,0,0,curses.LINES,curses.COLS)
        time.sleep(.01)
        pad.addstr(y,0,'*')
        pad.addstr(y,curses.COLS-1,'*')
    pad.addstr(curses.LINES-1,0,horizBorder[:-1])
    pad.refresh(0,0,0,0,curses.LINES,curses.COLS)



# Creates a new window, displays text centered around (y,x) and returns the window for potential usage
def textWindow(y,x,string):
    halfwidth = -1
    halfheight = -1
    linestrings = []
    max = -1
    linestrings = string.split("\n")
    lines = string.count("\n") + 1
    max = ""
    for s in linestrings:
        if len(s) > len(max):
            max = s
    max = len(max)
    halfwidth = (max+4)/2
    halfheight = (len(linestrings)+4)/2
    next = curses.newwin(4 + len(linestrings),4 + max,y-halfwidth,x-halfheight)
    next.box()
    pan = curses.panel.new_panel(next)
    for i in range(0,lines):
        next.addstr(i+2,2,linestrings[i])
    return (pan,next)
        


def mainMenu(stdscr):
    str = "ASCIIria Chronicles\n\n1 New Game\n\n2 Select Map\n\n3 Exit"
    (pan,win) = textWindow(curses.LINES/2,curses.COLS/2,str)
    pan.top()
    pad.addstr(curses.LINES-2,1,"v0.0.1 by Andrew Barry")
    win.refresh()
    while 1:
        time.sleep(0.1)

    return -1

# ends the program
def closeGame():
    curses.nocbreak(); 
    stdscr.keypad(0); 
    curses.echo()
    curses.endwin()

def main(stdscr):
    if (curses.LINES < 50 or curses.COLS < 150):
        closeGame()
        return
    drawBorders() # fancy border drawing effect
    choice = mainMenu(stdscr) # do main menu everything
    while 1:
        pad.refresh(0,0,0,0,curses.LINES,curses.COLS)
        


curses.wrapper(main)
