# ASCIIria Chronicles

# nbsp: 
# padrefresh(padstarty,padstartx,inwindowstarty,inwindowstartx,inwindowclosey,inwindowclosex)


import curses, time
from curses import wrapper, panel
from Scenario import Scenario
from Engine import Game
from Utilities import textWindow

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


# do main menu
def mainMenu():
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
            pan.hide()
            return maps[selection-1]
        elif (selection == 0):
            pan.hide()
            return "BACK"

# set color pairs to what I want
def initColors():
    curses.init_pair(1,curses.COLOR_RED,-1)
    curses.init_pair(4,curses.COLOR_BLUE,-1)
    curses.init_pair(7,curses.COLOR_BLUE,curses.COLOR_BLUE)


# ends the program
def closeGame():
    curses.nocbreak(); 
    stdscr.keypad(0); 
    curses.echo()
    curses.endwin()


# Starts the game
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
        choice = mainMenu() # do main menu everything
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
    menu.refresh(0,0,0,0,curses.LINES,curses.COLS)
    gamePad = scenario.map
    gamePad.refresh(0,0,10,(curses.COLS/2 - 10),20,curses.COLS/2)

    # START PLAYING!
    game = Game(scenario, 10, (curses.COLS/2 - 10)) # hardcoded numbers for now - This should be changed later to center in the window
    while 1:
        game.doNextTurn()


curses.wrapper(main)
