# Coordinates elements of a functioning game
# 
from Scenario import Scenario
from Unit import Unit
from Utilities import textWindow, cursorOnPositions
import curses

selectionChars = "0123456789abcdefghijklmnopqrstuvwxyz" # up to 36 units!
stdscr = curses.initscr()

class Game:
    # read list of available units from the text file units.txt
    def __init__(self,scenario, mapy, mapx, map,win):
        self.scenario = scenario
        self.mapy = mapy
        self.mapx = mapx
        self.map = map
        self.currentTurn = 0
        self.win = win
        file = open('units.list','r')
        lines = file.readlines()
        self.playerUnits = []
        for line in lines:
            attrs = line.split("/")
            pos = [-1,-1] # no position set yet!
            self.playerUnits.append(Unit(attrs[0],attrs[1],attrs[2],attrs[3],pos,True))
            
    # take turns
    def doNextTurn(self):
        if (self.currentTurn == 0):
            self.doPreGame()
            turn = 1
        elif (int(self.currentTurn) == self.currentTurn): # player turn
            #self.doPlayerTurn()
            self.currentTurn += .5
        else: # enemy turn
            #self.doEnemyTurn()
            self.currentTurn += .5


    # translate nums like (+y,+x) so that it is in context of the whole window 
    # (used when using a cursor to select anything in scenario.map)
    def translate(self,nums,y,x):
        new = [nums[0],nums[1]]
        new[0] += y
        new[1] += x
        return new

    # Pre-game: allow unit selections on self.scenario.openings[]
    def doPreGame(self):
        openspaces = self.scenario.openings
        while (len(openspaces) > 0):
            curses.panel.update_panels()
            self.win.refresh()
            self.map.refresh(0,0,10,(curses.COLS/2 - 10),20,curses.COLS/2)
            string = "Select " + str(len(openspaces)) + " more unit"
            if (len(openspaces) > 1): string += "s"
            string += ".\n\n\tName\tType\tHP\tAtt"
            for x in range(0,len(self.playerUnits)):
                unit = self.playerUnits[x]
                string = string + "\n" + selectionChars[x] + "\t" + unit.name + "\t" + unit.type + "\t" + str(unit.hp) + "\t" + str(unit.att) + "\n"
            (pan,msgbox) = textWindow(5,5,string,topLeft=True)
            msgbox.refresh()
            pan.top()
            c = 'placeholder'
            while (selectionChars.find(c) == -1):
                c = str(unichr(stdscr.getch()))
            selectedunit = self.playerUnits[selectionChars.find(c)]
            selectedposition = cursorOnPositions([self.translate(nums, 10, (curses.COLS/2 - 10)) for nums in openspaces],self.win)
            selectedunit.pos = openspaces[selectedposition] # give unit correct position
            openspaces.remove(openspaces[selectedposition]) # remove space from list
            self.scenario.addUnit(selectedunit) # add unit to map
            self.playerUnits.remove(selectedunit) # remove unit from list
            del pan
            del msgbox
            curses.panel.update_panels()
            self.win.refresh()
            self.map.refresh(0,0,10,(curses.COLS/2 - 10),20,curses.COLS/2)
