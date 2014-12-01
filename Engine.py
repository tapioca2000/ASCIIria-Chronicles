# Coordinates elements of a functioning game
# 
from Scenario import Scenario
from Unit import Unit
from Weapon import Weapon
from Utilities import *
import curses

unittypes = {"T":"Tank","S":"Scout","H":"sHocktrooper","L":"Lancer","E":"Engineer","N":"sNiper"} # full unit names
unitAPs = {"T":5,"S":15,"H":7,"L":5,"E":13,"N":6} # unit movement ranges

selectionChars = "0123456789abcdefghijklmnopqrstuvwxyz" # up to 36 units!
stdscr = curses.initscr()

class Game:
    # read list of available units from the text file units.txt
    def __init__(self,scenario, map):
        self.scenario = scenario
        self.mapy = scenario.mapy
        self.mapx = scenario.mapx
        self.map = map
        self.currentTurn = 0
        self.cp = 0
        file = open('units.list','r')
        lines = file.readlines()
        self.playerUnits = []
        for line in lines:
            attrs = line.split("/")
            pos = [-1,-1] # no position set yet!
            self.playerUnits.append(Unit(attrs[0],attrs[1],attrs[2],attrs[3],pos,True))
            self.cp += 1
            if (attrs[1] == 'T'): # CP boost while tank is alive (TODO: leader attribute)
                self.cp += 1
            
    # take turns
    def doNextTurn(self):
        if (self.currentTurn == 0):
            self.doPreGame()
            self.currentTurn += .5
        elif (int(self.currentTurn) == self.currentTurn): # player turn
            self.doPlayerTurn()
            self.currentTurn += .5
        else: # enemy turn
            self.doEnemyTurn()
            self.currentTurn += .5


    # Pre-game: allow unit selections on self.scenario.openings[]
    def doPreGame(self):
        self.weapons = readWeaponList("weapons.list")
        openspaces = self.scenario.openings
        while (len(openspaces) > 0): # unit placement loop
            self.scenario.updateMap()
            self.map = self.scenario.mapPan()
            curses.panel.update_panels()
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
            while (selectionChars[0:len(openspaces)].find(c) == -1):
                c = str(unichr(stdscr.getch()))
            del pan
            del msgbox
            selectedunit = self.playerUnits[selectionChars.find(c)]
            selectedposition = cursorOnPositions(openspaces,self.map.window())
            selectedunit.pos = self.scenario.openings[selectedposition] # give unit correct position
            openspaces.remove(openspaces[selectedposition]) # remove space from list
            self.scenario.addUnit(selectedunit) # add unit to map
            self.playerUnits.remove(selectedunit) # remove unit from list
            self.scenario.updateMap()
            self.map = self.scenario.mapPan()
            self.map.top()
            curses.panel.update_panels()

    # Do a player turn
    def doPlayerTurn(self):


        infoString = "[e] End Turn | [Arrow Keys] Select Unit | [Enter] Use Unit"
        thisTurnCP = self.cp
        cpString = "CP: " + ("X "*thisTurnCP)
        (cpPan,cpWin) = writeBar(3,1,curses.COLS-2,cpString)
        cpWin.refresh()
        cpPan.top()
        curses.panel.update_panels()
        highlightedunit = 0
        ch = 99
        
        redoInfo = False
        thisunit = self.scenario.friendlyunits[highlightedunit]
        unitinfo = "Name " + thisunit.name + "\nType " + unittypes[thisunit.type] + "\nHealth " + thisunit.hp + "\nAttack " + thisunit.att
        (unitPan,unitWin) = textWindow(20,20,unitinfo,topLeft=True)
        unitWin.refresh()

        while (ch != 101): # entire turn loop
            if (redoInfo): # change the unit info window
                del unitPan
                del unitWin
                curses.panel.update_panels()
                thisunit = self.scenario.friendlyunits[highlightedunit]
                unitinfo = "Name " + thisunit.name + "\nType " + unittypes[thisunit.type] + "\nHealth " + thisunit.hp + "\nAttack "+ thisunit.att
                (unitPan,unitWin) = textWindow(20,20,unitinfo,topLeft=True)
                unitWin.refresh()
                redoInfo = False
            self.scenario.updateMap()
            self.map = self.scenario.mapPan()
            self.map.window().chgat(thisunit.pos[0], thisunit.pos[1],1,curses.color_pair(3))
            self.map.window().refresh()
            (infoPan,infoWin) = writeBar(1,1,curses.COLS-2,infoString)
            (cpPan,cpWin) = writeBar(3,1,curses.COLS-2,cpString)
            cpWin.refresh()
            infoWin.refresh()


            curses.panel.update_panels()

            ch = stdscr.getch()

            redoInfo = (ch == curses.KEY_LEFT or ch == curses.KEY_RIGHT) # redo unit info panel if new unit selected
            if (ch == curses.KEY_LEFT): # Highlight unit on the left
                highlightedunit -= 1
                if (highlightedunit == -1): highlightedunit = len(self.scenario.friendlyunits) - 1
            elif (ch == curses.KEY_RIGHT): # Highlight unit on the right
                highlightedunit += 1
                if (highlightedunit == len(self.scenario.friendlyunits)): highlightedunit = 0
            elif (ch == 10 and thisTurnCP > 0): # Enter movement mode for this unit
                thisTurnCP -= 1
                cpString = "CP: " + ("X "*thisTurnCP)
                self.movementMode(self.scenario.friendlyunits[highlightedunit])

    # active movement of a unit
    def movementMode(self,unit):
        ap = unitAPs[unit.type]
        (infoPan,infoWin) = writeBar(1,1,curses.COLS-2,"[Arrow Keys] move | [F] fire | [S] switch weapon | [E] end movement")
        infoWin.refresh()
        infoPan.top()

        weaponSelectIndex = 0
        weaponlist = self.weapons[unit.type]
        selectedweapon = weaponlist[weaponSelectIndex]
        (wepPan,wepWin) = textWindow(30,10,"CURRENT WEAPON\nName " + selectedweapon.name + "\nRange " + selectedweapon.range + "\nAtt " + selectedweapon.att + "\nAcc " + selectedweapon.acc,topLeft=True)
        wepWin.refresh()


        ch = 99
        while (ch != 101):
            self.scenario.updateMap()
            self.map = self.scenario.mapPan()
            self.map.window().refresh()
            (apPan,apWin) = writeBar(3,1,curses.COLS-2,("AP: " + ("X "*ap)))
            apWin.refresh()
            curses.panel.update_panels()

            ch = stdscr.getch()

            if (ch == 102): # F was pressed, enter fire mode
                print("TODO")
            elif (ch == 115): # S was pressed, switch weapons
                weaponSelectIndex += 1
                if (weaponSelectIndex >= len(weaponlist)): weaponSelectIndex = 0
                selectedweapon = weaponlist[weaponSelectIndex]
                del wepPan
                del wepWin
                curses.panel.update_panels()
                (wepPan,wepWin) = textWindow(30,10,"CURRENT WEAPON\nName " + selectedweapon.name + "\nRange " + selectedweapon.range + "\nAtt " + selectedweapon.att + "\nAcc " + selectedweapon.acc,topLeft=True)
                wepWin.refresh()

            elif (ch == curses.KEY_LEFT): # move left
                if (freespace(self.scenario,[unit.pos[0],unit.pos[1]-1]) and ap > 0):
                    unit.move_left()
                    ap -= 1
            elif (ch == curses.KEY_RIGHT): # move right
                if (freespace(self.scenario,[unit.pos[0],unit.pos[1]+1]) and ap > 0):
                    unit.move_right()
                    ap -= 1
            elif (ch == curses.KEY_UP): # move up
                if (freespace(self.scenario,[unit.pos[0]-1,unit.pos[1]]) and ap > 0):
                    unit.move_up()
                    ap -= 1
            elif (ch == curses.KEY_DOWN): # move down
                if (freespace(self.scenario,[unit.pos[0]+1,unit.pos[1]]) and ap > 0):
                    unit.move_down()
                    ap -= 1
    
    # do the enemy's turn. A bit like doPlayerTurn but not exactly.
    def doEnemyTurn(self):
        (textPan,textWin) = textWindow(curses.LINES/2,curses.COLS/2,"Enemy turn")
        textWin.refresh()
        curses.panel.update_panels()
        stdscr.getch()
        del textPan
        del textWin
