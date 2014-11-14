import os
import platform
import random
import sys
import time
import console as con
from player import *
from classAttr import *
from pycompat import *
from mapData import *

############################
#### Set up environment ####
con.set_text_color(con.darkgreen, con.black)
con.clear_screen()

############################
######## Constants #########
HP_BASE_MOD  = 50
HP_MULT      = 4.5
LUCK_MOD     = 4.0
MISS_BASE    = 10
MISS_MOD     = 1
REROLL_MOD   = .85
WPN_STAT_MOD = 800.0

############################
######### Globals ##########
prompt = ">>> "
debug = False
# player (defined in startGame())

############################
### Beginning Functions ####
def startGame():
    global player

    openingStory() 
    while True: # Main loop
        titleMenu()
        player = createCharacter()
        playGame()
    # Draw main game screen
    # ...

def openingStory():
    print ("\n"
           "\n\t      Adventures of Grogg?\n"
           "\n\t  Eventually, there will be a short"
           "\n\tintroductory narrative here. For now,"
           "\n\tyou'll just have to do without.\n"
           "\n\t  No, no. Please don't cry. It won't"
           "\n\tbe too long - we promise! I know you"
           "\n\tcan't wait.\n"
           "\n\t ....."
           "\n\t"
           "\n\t")
    pause()
    con.clear_screen()

def titleMenu():
    global debug

    print ("\n"
           "\n\t      Adventures of Grogg?"
           "\n\tWelcome to the greatest text-based"
           "\n\t  adventure you have ever played."
           "\n\n")
    print (" 1. Start\n" 
           " 2. Options\n"
           " 3. Exit\n\n")
    
    startSelected = False
    while not startSelected:
        choice = input(prompt)
        
        if choice.lower() in ("start", "s", "1"):
            startSelected = True
        elif choice.lower() in ("options", "o", "2"):
            optionsMenu()
        elif choice.lower() in ("exit", "e", "3"):
            con.clear_color()
            con.clear_screen()
            exit()
        elif choice.lower() == "debug":
            debug = True
            debugMsg("Debug messages enabled")
        else:
            print("\nThats not an option!\n")
    
    con.clear_screen()

def optionsMenu():
    con.clear_screen()

    print ("\n"
           "\n\t      Options Menu!"
           "\n\n")
    print (" 1. Change default prompt (%s)\n") % prompt
    print (" 2. ...\n")
    print (" 3. Back to Main Menu\n\n")

    pause() # Temporary

    # TODO: 
    #   - Flesh out options
    #   - If DEBUG, have options to change things
    #       like battle constants. Options for all
    #       the things!

    con.clear_screen()

############################
#### Character Creation ####
def createCharacter():
    name = createName()
    attr, gear = classSelect(name)
    attr = allocStats(attr, name)
    return Player(name, attr, gear)

def createName():
    print (" What do you call yourself, adventurer?\n\n")
    name = input(prompt)
    con.clear_screen()
    return name

def classSelect(name):
    valid = False
    while not valid:
        print (" Choose your path, %s!\n") % name
        print (" 1. Warrior\n"
               " 2. Knight\n"
               " 3. Royalty\n"
               " 4. Mage\n"
               " 5. Thief\n"
               " 6. Hunter\n\n")
        choice = input(prompt)

        if choice.lower() in ("warrior", "w", "1"):
            attr, gear = warriorAttr()
            valid = True
        elif choice.lower() in ("knight", "k", "2"):
            attr, gear = knightAttr()
            valid = True
        elif choice.lower() in ("royalty", "r", "3"):
            attr, gear = royaltyAttr()
            valid = True
        elif choice.lower() in ("mage", "m", "4"):
            attr, gear = mageAttr()
            valid = True
        elif choice.lower() in ("thief", "t", "5"):
            attr, gear = thiefAttr()
            valid = True
        elif choice.lower() in ("hunter", "h", "6"):
            attr, gear = hunterAttr()
            valid = True

    con.clear_screen()
    return attr, gear

def allocStats(attr, name):
    points = 10

    pvit = attr["vit"]
    pend = attr["end"]
    pint = attr["int"]
    pstr = attr["str"]
    pdex = attr["dex"]
    pmag = attr["mag"]
    pfth = attr["fth"]
    plck = attr["lck"]

    print (" Do you have any specific training?\n\n"
           "  This is were you can give your\n"
           "character a name and allocate any\n"
           "skill points you have. You start\n"
           "with a total of 10 points to\n"
           "allocate to any attribute you see\n"
           "fit.\n\n")
    pause()
    
    charMenu = True
    while charMenu:
        con.clear_screen()
        print ("   Name: %s\n\n"
               "   Vitality ...... %d\n"
               "   Intelligence .. %d\n"
               "   Endurance ..... %d\n"
               "   Strength ...... %d\n"
               "   Dexterity ..... %d\n"
               "   Magicka ....... %d\n"
               "   Faith ......... %d\n"
               "   Luck .......... %d\n\n"
               "   Points: %d\n\n") % (name, pvit, pend, 
                                       pint, pstr, pdex, 
                                       pmag, pfth, plck, 
                                       points)
        print ("1. Spend Points\n"
               "2. Remove Points\n"
               "3. Done!\n\n")
        choice = input(prompt)

        if choice.lower() in ("spend", "s", "1"):
            
            con.clear_screen()

            print ("   Name: %s\n\n"
                   "1. Vitality ...... %d\n"
                   "2. Intelligence .. %d\n"
                   "3. Endurance ..... %d\n"
                   "4. Strength ...... %d\n"
                   "5. Dexterity ..... %d\n"
                   "6. Magicka ....... %d\n"
                   "7. Faith ......... %d\n"
                   "8. Luck .......... %d\n\n"
                   "   Points: %d\n\n") % (name, pvit, pend, 
                                           pint, pstr, pdex, 
                                           pmag, pfth, plck, 
                                           points)
            statChoice = input(prompt)

            validChoice = [["vitality", "vit", "v", "1"],
                           ["intelligence", "int", "i", "2"], 
                           ["endurance", "end", "e", "3"], 
                           ["strength", "str", "s", "4"],
                           ["dexterity", "dex", "d", "5"],
                           ["magicka", "mag", "m", "6"],
                           ["faith", "fth", "fai", "f", "7"],
                           ["luck", "lck", "luc", "l", "8"]]
            
            if ( statChoice in x for x in validChoice ):
                print ("Add how many points?")
                numPoints = int(input(prompt))
                if numPoints > points:
                    print ("What exactly are you trying to achieve?")
                    pause()
                elif numPoints < 0:
                    print ("I'm not doing that...?")
                    pause()
                elif numPoints == 0:
                    print ("What are you trying to do?")
                    pause()
                else:                
                    if   statChoice in validChoice[0]: # vit
                        pvit += numPoints
                        points -= numPoints
                    elif statChoice in validChoice[1]: # int
                        pend += numPoints
                        points -= numPoints
                    elif statChoice in validChoice[2]: # end
                        pint += numPoints
                        points -= numPoints
                    elif statChoice in validChoice[3]: # str
                        pstr += numPoints
                        points -= numPoints
                    elif statChoice in validChoice[4]: # dex
                        pdex += numPoints
                        points -= numPoints
                    elif statChoice in validChoice[5]: # mag
                        pmag += numPoints
                        points -= numPoints
                    elif statChoice in validChoice[6]: # fth
                        pfth += numPoints
                        points -= numPoints
                    elif statChoice in validChoice[7]: # lck
                        plck += numPoints
                        points -= numPoints
            else:
                print("Invalid option.")
                pause()

        elif choice.lower() in ("remove", "rm", "r", "2"):
            
            con.clear_screen()

            print ("   Name: %s\n\n"
                   "1. Vitality ...... %d\n"
                   "2. Intelligence .. %d\n"
                   "3. Endurance ..... %d\n"
                   "4. Strength ...... %d\n"
                   "5. Dexterity ..... %d\n"
                   "6. Magicka ....... %d\n"
                   "7. Faith ......... %d\n"
                   "8. Luck .......... %d\n\n"
                   "   Points: %d\n\n") % (name, pvit, pend, 
                                           pint, pstr, pdex, 
                                           pmag, pfth, plck, 
                                           points)
            statChoice = input(prompt)

            validChoice = [["vitality", "vit", "v", "1"],
                           ["intelligence", "int", "i", "2"], 
                           ["endurance", "end", "e", "3"], 
                           ["strength", "str", "s", "4"],
                           ["dexterity", "dex", "d", "5"],
                           ["magicka", "mag", "m", "6"],
                           ["faith", "fth", "fai", "f", "7"],
                           ["luck", "lck", "luc", "l", "8"]]
            
            if any( statChoice in x for x in validChoice ):
                print ("Subtract how many points?")
                numPoints = int(input(prompt))
                if numPoints > points:          # TODO: Fix this logic
                    print ("What exactly are you trying to achieve?")
                    pause()
                elif numPoints < 0:
                    print ("I'm not doing that...?")
                    pause()
                elif numPoints == 0:
                    print ("What are you trying to do?")
                    pause()
                else:                
                    if   statChoice in validChoice[0]: # vit
                        pvit -= numPoints
                        points += numPoints
                    elif statChoice in validChoice[1]: # int
                        pend -= numPoints
                        points += numPoints
                    elif statChoice in validChoice[2]: # end
                        pint -= numPoints
                        points += numPoints
                    elif statChoice in validChoice[3]: # str
                        pstr -= numPoints
                        points += numPoints
                    elif statChoice in validChoice[4]: # dex
                        pdex -= numPoints
                        points += numPoints
                    elif statChoice in validChoice[5]: # mag
                        pmag -= numPoints
                        points += numPoints
                    elif statChoice in validChoice[6]: # fth
                        pfth -= numPoints
                        points += numPoints
                    elif statChoice in validChoice[7]: # lck
                        plck -= numPoints
                        points += numPoints
            else:
                print("Invalid option.")
                pause()

        elif choice.lower() in ("done", "d", "3"):
            charMenu = False
        else:
            print("Incorrect input")
            pause()
    
    con.clear_screen()
    
    attr["vit"] = pvit
    attr["end"] = pend
    attr["int"] = pint
    attr["str"] = pstr
    attr["dex"] = pdex
    attr["mag"] = pmag
    attr["fth"] = pfth
    attr["lck"] = plck

    return attr

############################
#### Gameplay Functions ####
def playGame():
    player.spawnRandom()

    quitToMenu = False # Eventually add pause/quit feature
    while not quitToMenu:
        con.clear_screen()
        
        drawStatWindow()
        drawMap()
        drawGuideWindow()
        pause() # temp
        
        # moveChar()

def drawStatWindow():
    pvit = player.attr["vit"]
    pend = player.attr["end"]
    pint = player.attr["int"]
    pstr = player.attr["str"]
    pdex = player.attr["dex"]
    pmag = player.attr["mag"]
    pfth = player.attr["fth"]
    plck = player.attr["lck"]
    pwpn = player.gear["wpn"]
    parm = player.gear["arm"]
    #           1         2         3         4         5         6         7         8
    #       .........!.........!.........!.........!.........!.........!.........!.........!
    print ("+------------------------------------------------------------------------------+")
    print ("| Stats:     |                     Player name: {:<30s} |".format( player.name ))
    print ("|     HP     | Vit | End | Int | Str | Dex | Mag | Fth | Lck | Wpn | Arm |     |")
    print ("|  {:^8.1f}  | {:^3d} | {:^3d} | {:^3d} | {:^3d} | {:^3d} "
           "| {:^3d} | {:^3d} | {:^3d} | {:^3d} | {:^3d} |     |\n"
           "+------------------------------------------------------------------------------+"
           "\n".format(player.hp, pvit, pend, pint, pstr, pdex, pmag, pfth, plck, pwpn, parm))

def drawGuideWindow():
    #           1         2         3         4         5         6         7         8
    #       .........!.........!.........!.........!.........!.........!.........!.........!
    print ("+------------------------------------------------------------------------------+")
    print ("| Legend:        |  Mountain  |  Goblin  |  Chest  |  GuardedChest  |  Player  |")
    print ("|                |     %s      |     %s    |    %s    |       %s        |     %s    |") % (M, G, C, X, P )
    print ("+------------------------------------------------------------------------------+")
    print ("| Controls:    |      Up       |      Down     |     Left      |     Right     |")
    print ("|              |       w       |        s      |       a       |       d       |")
    print ("+------------------------------------------------------------------------------+")
    print ("")

def drawMap():
    posx = player.pos[0]
    posy = player.pos[1]

    for y in range(len(terMap)):
        sys.stdout.write("\t     ")
        for x in range(len(terMap[y])):
            current = terMap[y][x]

            ## Place player on map
            if posx == x and posy == y:
                out = unicode(P+" ")
            ## Handle some awkward conditions
            elif current == H or current == L or current == F:
                out = unicode(current)+H
            elif current == D:
                out = "\b" + (unicode("-")*3)
            ## For all other terrain
            else: 
                out = unicode(current)+u" "
            
            ## Write out current tile as built above
            sys.stdout.write(out)
        print ('')

def movement():
    pass

############################
#### Utility Functions #####
def debugMsg(s):
    if debug:
        con.set_text_color(con.darkred, con.black)
        print ('[DEBUG]: %s' % s)
        con.set_text_color(con.darkgreen, con.black)

def pause(msg = "Press Enter to Continue... "):
    input(" " + msg)

# TODO: Rewrite old Functions:
   # calcHP ............ in progress
   # attack ............ in progress
   # battle ............ in progress
   
   # spawnPlayer ....... done
   # terrain ........... done
   
   # change_direction .. done
   # is_collision ...... done
   # moveChar .......... done
   
   # skillAlloc ........ done
   # charSelect ........ done
   
   # playGame .......... done
   # menu .............. done
############################
############################

if __name__ == "__main__":
    startGame()
    drawMap()
    pause()
    con.clear_color()
    con.clear_screen()

