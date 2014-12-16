# Coordinates elements of a functioning game
# most of the game happens here
 
from Scenario import Scenario
from Unit import Unit
from Weapon import Weapon
from Utilities import *
from time import sleep
import curses
import math

# important general information on unit types
unittypes = {"T":"Tank","S":"Scout","H":"sHocktrooper","L":"Lancer","E":"Engineer","N":"sNiper"} # full unit names
unitAPs = {"T":5,"S":15,"H":7,"L":5,"E":13,"N":6} # unit movement ranges
unitACCs = {"T":.6,"S":8,"H":.6,"L":.5,"E":.7,"N":.8} # unit base accuracies
unitRanges = {"T":7,"S":5,"H":4,"L":4,"E":3,"N":9} # unit ranges

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
        self.enemycp = 4
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
            self.currentTurn += 1
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
            while (selectionChars[0:len(self.playerUnits)+1].find(c) == -1):
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
        unitinfo = "Name " + thisunit.name + "\nType " + unittypes[thisunit.type] + "\nHealth " + str(thisunit.hp) + "\nAttack " + str(thisunit.att)
        (unitPan,unitWin) = textWindow(20,20,unitinfo,topLeft=True)
        unitWin.refresh()

        while (ch != 101): # entire turn loop
            if (redoInfo): # change the unit info window
                del unitPan
                del unitWin
                curses.panel.update_panels()
                thisunit = self.scenario.friendlyunits[highlightedunit]
                unitinfo = "Name " + thisunit.name + "\nType " + unittypes[thisunit.type] + "\nHealth " + str(thisunit.hp) + "\nAttack "+ str(thisunit.att)
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
        del cpPan
        del cpWin
        del unitPan
        del unitWin
        del infoPan
        del infoWin
        curses.panel.update_panels()

    # active movement of a unit
    def movementMode(self,unit,moveList=None):
        ap = unitAPs[unit.type]
        (infoPan,infoWin) = writeBar(1,1,curses.COLS-2,"[Arrow Keys] move | [F] fire | [S] switch weapon | [E] end movement")
        infoWin.refresh()
        infoPan.top()

        weaponSelectIndex = 0
        weaponlist = self.weapons[unit.type]
        selectedweapon = weaponlist[weaponSelectIndex]
        (wepPan,wepWin) = textWindow(30,10,"CURRENT WEAPON\nName " + selectedweapon.name + "\nRange " + str(selectedweapon.range) + "\nAtt " + str(selectedweapon.att) + "\nAcc " + str(selectedweapon.acc),topLeft=True)
        wepWin.refresh()


        ch = 99
        counter = 0
        while (ch != 101):
            self.scenario.updateMap()
            self.map = self.scenario.mapPan()
            self.map.window().refresh()
            (apPan,apWin) = writeBar(3,1,curses.COLS-2,("AP: " + ("X "*ap)))
            apWin.refresh()
            curses.panel.update_panels()
            if not moveList:
                ch = stdscr.getch()
            else:
                ch = moveList[counter]
                counter += 1
                sleep(.75)
            if (ch == 102): # F was pressed, enter fire mode
                if not moveList:
                    self.fireMode(unit,selectedweapon)
                else:
                    counter += 1
                    self.fireMode(unit,selectedweapon,moveList[counter])
                    counter += 1
            elif (ch == 115): # S was pressed, switch weapons
                weaponSelectIndex += 1
                if (weaponSelectIndex >= len(weaponlist)): weaponSelectIndex = 0
                selectedweapon = weaponlist[weaponSelectIndex]
                del wepPan
                del wepWin
                curses.panel.update_panels()
                (wepPan,wepWin) = textWindow(30,10,"CURRENT WEAPON\nName " + selectedweapon.name + "\nRange " + str(selectedweapon.range) + "\nAtt " + str(selectedweapon.att) + "\nAcc " + str(selectedweapon.acc),topLeft=True)
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
        del wepPan
        del wepWin
        curses.panel.update_panels()
    
    # do the enemy's turn. Select what we want to do, select who to do it, do it.
    def doEnemyTurn(self):
        thisTurnCP = self.enemycp
        cpStr = "CP: " + ("X "*thisTurnCP)
        (cpPan,cpWin) = writeBar(1,3,curses.COLS-2,cpStr)
        cpWin.refresh()
        curses.panel.update_panels()
        while (thisTurnCP > 0):
            moveType = self.determineMove() # 0 - defend flag, 1 - attack enemy flag, 2 - attack unit, 3 - heal tank
            uI,target = self.getBestUnit(moveType)
            if not uI: continue
            unit = self.scenario.enemyunits[uI]
            movelist = self.getMoves(moveType,unit,target)
            self.movementMode(unit,moveList=movelist)
            thisTurnCP -= 1
    def determineMove(self): # Step 1 - determine the type of move to do
        movetype = 0
        tanks = [x for x in self.scenario.enemyunits if x.type = 'T']
        for tank in tanks:
            if tank.hp <= 500: return 3 # tank needs healing
        eflag = self.scenario.eflag
        pflag = self.scenario.pflag
        pflagUnattended = True
        eflagUnattended = True
        for unit in (self.scenario.enemyunits + self.scenario.playerunits):
            pflagdist = math.sqrt(math.pow(pflag[0] - unit.pos[0],2) + math.pow(pflag[1] - unit.pos[1],2))
            eflagdist = math.sqrt(math.pow(eflag[0] - unit.pos[0],2) + math.pow(pflag[1] - unit.pos[1],2))
            if (unit.friendly and pflagdist < 10):
                pflagUnattended = False
            elif (unit.friendly and eflagdist < 5 and not eflagUnattended): # active flag defense
                return 2
            elif (unit.friendly and eflagdist < 5): # move to defend flag
                return 0
        if pflagUnattended: # player flag is unattended, attack it
            return 1
        return 2 # unsure of what to do, attack something
    def getBestUnit(self,movetype): # step 2 - determine the unit to do the move
        if (movetype == 0 or movetype == 1): # defend/attack the flag - select best unit for the job
            if (movetype == 0): flag = self.scenario.eflag
            else: flag = self.scenario.pflag
            weights = [0 for x in self.scenario.enemyunits]
            minUnitI = 0
            minDist = -1
            maxStr = 0
            maxStrI = 0
            for x in range(0,len(weights)):
                unit = self.scenario.enemyunits[x]
                flagdist = math.sqrt(math.pow(flag[0] - unit.pos[0],2) + math.pow(flag[1] - unit.pos[1],2))
                if (flagdist < minDist):
                    minUnitI = x
                    minDist = flagdist
                str = unit.att
                if (str > maxStr):
                    maxStrI = x
                    maxStr = str
            weights[minUnitI] += 3
            weights[maxStrI] += 2
            overallMaxI = 0
            for x in range(0,len(weights)):
                if (weights[x] > weights[overallMaxI]):
                    overallMaxI = x
            return overallMaxI, flag
        elif (movetype == 3): # heal the tank - find the engineer
            injuredTank = None
            tanks = [x for x in self.scenario.enemyunits where x.type == 'T']
            for tank in tanks:
                if tank.hp < 500: injuredTank = tank
            pos = injuredTank.pos
            engineers = [x for x in self.scenario.enemyunits where x.type == 'E']
            mindist = 0
            mindistI = 0
            for x in range(0,len(engineers)):
                eng = engineers[x]
                dist = math.sqrt(math.pow(pos[0] - eng.pos[0],2) + math.pow(pos[1] - eng.pos[1],2))
                if (dist < mindist):
                    mindist = dist
                    mindistI = x
            return mindistI,pos
        elif (movetype == 2): # attack another unit
            weights = [0 for x in self.scenario.enemyunits]
            targets = {}
            c = 0
            for unit in self.scenario.enemyunits:
                pos = unit.pos
                closestunit = None
                closestdist = 999999
                for punit in self.scenario.friendlyunits:
                    dist = Math.sqrt(Math.pow(punit.pos[0] - pos[0],2) + Math.pow(punit.pos[1] - pos[1],2))
                    if (dist < closestdist):
                        closestunit = punit
                        closestdist = dist
                if not closestunit: continue
                targets[unit] = closestunit
                if (closestdist > 10): # too far, ignore
                    weights[c] = -999
                else:
                    weights[c] += (unit.att - closestunit.att)
                c += 1
            maxI = 0
            for x in range(0,len(weights)):
                if (weights[x] > weights[0]):
                    maxI = x
            if maxI < 0: return [None,None] # don't do it, there are no units that can attack.
            return [maxI,targets[self.scenario.enemyunits[maxI]]]
    def getMoves(self,movetype,unit,target): # step 3 - generate the actions the unit should take
        poslist = pathfind(unit.pos,target)
        if (movetype == 3):
            poslist.append(switchToWrench(self))
            poslist.append('F')
            poslist.append(target)
        elif (movetype == 2):
            poslist += self.switchToStrongestWeapon(unit.type))
            poslist.append('F')
            poslist.append(target)
        elif (movetype == 1):
            poslist.append('T')
        return poslist
    def pathfind(start,end): # find the shortest path!
        print("TODO!!! It'll be djikstra's algorithm")
    def switchToStrongestWeapon(self,type):
        maxwep = self.weapons[type][0]
        maxI = 0
        c = 0
        for weapon in self.weapons[type]:
            if weapon.att > maxwep.att:
                maxwep = weapon
                maxI = c
            c += 1
        return [115]*maxI
    def switchToWrench(self):
        cmd = []
        for weapon in self.weapon[type]:
            if (weapon.name == "Wrench"): return cmd
            cmd.append(115)
        return []

    # unit attack mode
    def fireMode(self,unit,weapon,target=None):
        infoString = "[E] exit | [Enter] fire | [Arrow Kews] adjust aim"
        (infoPan,infoWin) = writeBar(1,1,curses.COLS-2,infoString)
        infoWin.refresh()
        height, width = self.map.window().getmaxyx()
        positions = []
        praw = []
        theta = 0
        r = unitRanges[unit.type] + weapon.range
        while (theta < 360):
            x = int(r*math.cos(math.radians(theta))) + unit.pos[1]
            y = int(r*math.sin(math.radians(theta))) + unit.pos[0]
            if (y >= 0 and y < height and x >= 0 and x < width-1):
                positions.append([y,x])
                self.map.window().chgat(y,x,1,curses.color_pair(5))
            praw.append([x,y]) # every position on the edge of the circle, regardless of whether or not it's in bounds
            theta += 10
        for x in range(0,width-1):
            for y in range(0,height):
                if (point_inside_polygon(x,y,praw)):
                    positions.append([y,x])
                    self.map.window().chgat(y,x,1,curses.color_pair(5)) # fill in the circle
        self.map.window().refresh()
        curses.panel.update_panels()
        positions = removeDupes(positions)
        spot = cursorOnPositions(positions, self.map.window()) # fire on this spot
        self.scenario.updateMap()
        self.map = self.scenario.mapPan()
        self.map.window().refresh()
        curses.panel.update_panels()
        targetunit = self.scenario.unitAtPosition(positions[spot])
        att = unit.att + weapon.att
        acc = unitACCs[unit.type] + weapon.acc
        if targetunit: # unit present at spot
            targetunit.attacked(acc,att,unit.type)
        del infoPan
        del infoWin
        curses.panel.update_panels()
