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

# do main menu
def mainMenu():
    string = "ASCIIria Chronicles\n\n1 New Game\n\n2 Select Map\n\n3 Exit"
    (pan,win) = textWindow(curses.LINES/2,curses.COLS/2,string)
    pan.top()
    win.refresh()
    while 1:
        c = stdscr.getch()
        selection = c-48
        if (selection==1 or selection==2 or selection==3): # return choice
            del pan
            del win
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
            del pan
            del win
            return maps[selection-1]
        elif (selection == 0):
            del pan
            del win
            return "BACK"

# set color pairs to what I want
def initColors():
    curses.init_pair(1,curses.COLOR_RED,-1) # red (typically denotes enemy unit)
    curses.init_pair(2,curses.COLOR_WHITE,curses.COLOR_BLACK) # white on black (for text bars)
    curses.init_pair(3,curses.COLOR_BLACK,curses.COLOR_YELLOW) # black on yellow (highlighting)
    curses.init_pair(4,curses.COLOR_BLUE,-1) # blue (typically denotes player unit)
    curses.init_pair(5,curses.COLOR_BLACK,curses.COLOR_GREEN) # black on green (highlighting)
    curses.init_pair(7,curses.COLOR_BLUE,curses.COLOR_BLUE) # blue on blue (water)

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
    mapx = (curses.COLS/2) - 10
    mapy = 10
    scenario = Scenario(filename,mapy,mapx) # Create the scenario
    
    mapPan = scenario.mapPan()
    mapPan.bottom()
    mapPan.move(mapy,mapx)
    curses.panel.update_panels()

    # START PLAYING!
    game = Game(scenario, mapPan)
    while 1:
        game.doNextTurn()


curses.wrapper(main)
