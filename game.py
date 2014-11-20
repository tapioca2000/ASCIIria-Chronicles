# ASCIIria Chronicles

# nbsp: 

import curses, time
from curses import wrapper, panel
from Scenario import Scenario

maps = ["Test Map"] # TODO: generate this list by reading for .scn files
stdscr = curses.initscr()
curses.curs_set(0)
menu = curses.newpad(curses.LINES,curses.COLS) # field

# draw the borders around the screen, fancily
def drawBorders(char='#'):
    horizBorder = char * (curses.COLS)
    menu.addstr(0,0,horizBorder)
    for y in range(1,curses.LINES-1):
        menu.refresh(0,0,0,0,curses.LINES,curses.COLS)
        time.sleep(.01)
        menu.addstr(y,0,char)
        menu.addstr(y,curses.COLS-1,char)
    menu.addstr(curses.LINES-1,0,horizBorder[:-1])
    menu.refresh(0,0,0,0,curses.LINES,curses.COLS)



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
        if len(s) > len(max):
            max = s
    max = len(max)
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

# do main menu
def mainMenu(stdscr):
    string = "ASCIIria Chronicles\n\n1 New Game\n\n2 Select Map\n\n3 Exit"
    (pan,win) = textWindow(curses.LINES/2,curses.COLS/2,string)
    menu.addstr(curses.LINES-2,1,"v0.0.1 by Andrew Barry",curses.color_pair(1))
    pan.top()
    menu.refresh(0,0,0,0,curses.LINES,curses.COLS)
    win.refresh()
    while 1:
        c = stdscr.getch()
        selection = c-48
        if (selection==1 or selection==2 or selection==3): # return choice
            return selection
    return -1

# do map selection
def mapSelect():
    display = "SELECT YOUR MAP\n"
    c = 1
    for map in maps:
        display = display + "\n" + str(c) + " " + map + "\n"
        c += 1
    display = display + "\n0 Back"
    (pan,win) = textWindow(10,10,display,topLeft=True)
    pan.top()
    win.refresh()
    while 1:
        c = stdscr.getch()
        selection = c-48
        if (selection <= len(maps) and selection > 0):
            return maps[selection-1]
        elif (selection == 0):
            return "BACK"

# set color pairs to what I want
def initColors():
    curses.init_pair(1,curses.COLOR_RED,-1)
    curses.init_pair(4,curses.COLOR_BLUE,-1)
    curses.init_pair(7,curses.COLOR_BLUE,-1)

# ends the program
def closeGame():
    curses.nocbreak(); 
    stdscr.keypad(0); 
    curses.echo()
    curses.endwin()


# Coordinates the whole game
def main(stdscr):
    if (curses.LINES < 50 or curses.COLS < 150):
        closeGame()
        return
    curses.start_color()
    curses.use_default_colors()
    initColors()
    drawBorders() # fancy border drawing effect
    loadgame = True
    while loadgame: # MAIN MENU LOOP
        choice = mainMenu(stdscr) # do main menu everything
        selectedMap = 0
        if (choice == 3):
            closeGame()
            return
        elif (choice == 1): # user has started a new game, go to first map
            selectedMap = maps[0]
        elif (choice == 2):
            selectedMap = mapSelect()
        loadgame = selectedMap is "BACK"
    filename = selectedMap.replace(" ","") + ".scn"
    scenario = Scenario(filename) # Create the scenario
    pad = scenario.map
    menu.refresh(0,0,0,0,curses.LINES,curses.COLS)
    while 1:
        pad.refresh(0,0,10,10,20,20)


curses.wrapper(main)
