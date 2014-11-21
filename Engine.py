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
    def __init__(self,scenario, mapy, mapx):
        self.scenario = scenario
        self.mapy = mapy
        self.mapx = mapx
        self.currentTurn = 0
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
        out = open('out.txt','w')
        openspaces = self.scenario.openings
        string = "Select " + str(len(openspaces)) + " more units.\n\n\tName\tType\tHP\tAtt"
        for x in range(0,len(self.playerUnits)):
            unit = self.playerUnits[x]
            string = string + "\n" + selectionChars[x] + "\t" + unit.name + "\t" + unit.type + "\t" + str(unit.hp) + "\t" + str(unit.att) + "\n"
        (pan,win) = textWindow(5,5,string,topLeft=True)
        win.refresh()
        pan.top()
        c = 'placeholder'
        while (selectionChars.find(c) == -1):
            c = str(unichr(stdscr.getch()))
        selectedunit = self.playerUnits[selectionChars.find(c)]
        selectedposition = cursorOnPositions(openspaces,self.scenario.map)
        # place unit here
        openspaces.remove(selectedposition) # no longer free
