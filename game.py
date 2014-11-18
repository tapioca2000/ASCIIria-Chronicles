# ASCIIria Chronicles v0.0.1
# Silly game by ME! Based on Valkyria Chronicles by SEGA


import curses, time
from curses import wrapper
stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
stdscr.keypad(True)
curses.curs_set(0)
pad = curses.newpad(curses.LINES,curses.COLS) # field

# refresh
def refresh():
    pad.refresh(0,0,0,0,curses.LINES,curses.COLS)

# draw the borders around the screen, fancily
def drawBorders():
    horizBorder = '*' * curses.COLS
    pad.addstr(0,0,horizBorder)
    for y in range(1,curses.LINES-1):
        refresh()
        time.sleep(.01)
        pad.addstr(y,0,'*')
        pad.addstr(y,curses.COLS-1,'*')
    pad.addstr(curses.LINES-2,0,horizBorder)

def mainMenu(stdscr):
    sx = (curses.COLS/2)-(len("ASCIIria Chronicles")/2)
    pad.addstr(curses.LINES/2,sx,"ASCIIria Chronicles")
    pad.addstr(curses.LINES/2 + 2,sx,"1 New Game")
    pad.addstr(curses.LINES/2 + 4,sx,"2 Select Map")
    pad.addstr(curses.LINES/2 + 6,sx,"3 Exit")
    pad.addstr(curses.LINES-3,1,"v0.0.1 by Andrew Barry")
    while 1:
        pad.refresh(0,0,0,0,curses.LINES,curses.COLS)
    return -1

def main(stdscr):
    drawBorders() # fancy border drawing effect
    choice = mainMenu(stdscr) # do main menu everything
    while 1:
        pad.refresh(0,0,0,0,curses.LINES,curses.COLS)
        


curses.wrapper(main)
