import os
import platform
import random
import sys
import time
import console as con
from classAttr import *
from pycompat import *

con.set_text_color(con.darkgreen, con.black)

# Map Entities
M = "^"       # Mountion/Rocks
G = "&"       # Static Goblin
R = "&"       # Random Goblin
C = "#"       # Treasure Chest
X = "%"       # Guarded Chest
e = " "       # Empty Space
D = u"\u2504" # Door
P = "P"       # Player

# Walls
V = u"\u2551" # vertical
H = u"\u2550" # horizontal
L = u"\u255A" # bottom-left
J = u"\u255D" # bottom-right
F = u"\u2554" # top-left
T = u"\u2557" # top-right
obsticles = [M, V, H, L, J, F, T]
                                           ####_V_MAP_V_####
         # 0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24
terMap = [[M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M,], #00
          [M, M, M, M, M, M, M, M, M, M, M, F, H, H, H, H, H, H, H, H, H, H, H, T, M,], #01
          [M, M, M, e, M, M, M, M, M, M, M, V, F, T, e, e, e, e, e, e, e, F, T, V, M,], #02
          [M, M, M, e, e, M, e, e, M, M, M, V, L, J, F, H, H, H, H, H, T, L, J, V, M,], #03
          [M, M, e, e, e, e, e, e, e, M, e, V, F, T, V, F, H, H, H, T, V, F, T, V, M,], #04
          [M, M, e, e, e, e, e, e, e, C, e, V, L, J, V, V, e, e, e, V, V, L, J, V, M,], #05
          [M, M, e, e, e, e, e, e, e, e, M, V, F, T, V, V, e, e, e, V, V, F, T, V, M,], #06
          [M, M, M, e, e, e, e, e, e, M, M, V, L, J, V, V, e, e, e, V, V, L, J, V, M,], #07
          [M, M, e, e, e, e, e, R, e, e, M, V, F, T, V, L, H, H, H, J, V, F, T, V, M,], #08
          [M, M, e, e, e, e, e, e, e, e, e, V, L, J, L, H, H, H, H, H, J, L, J, V, M,], #09
          [M, M, e, e, e, e, e, e, e, e, e, V, F, H, T, e, e, e, e, e, F, H, T, V, M,], #10
          [M, M, M, e, e, e, e, e, e, X, e, V, V, e, V, F, H, D, H, T, V, e, V, V, M,], #11
          [M, M, M, e, e, e, e, e, e, e, e, V, L, H, J, V, e, G, e, V, L, H, J, V, M,], #12
          [M, M, M, e, e, e, e, e, e, e, e, L, H, H, H, J, e, e, e, L, H, H, H, J, M,], #13
          [M, M, e, e, e, e, X, e, e, e, e, e, e, e, e, e, e, e, e, e, e, e, C, M, M,], #14
          [M, M, M, e, e, e, e, e, e, e, e, e, e, e, e, e, e, e, e, e, e, e, e, M, M,], #15
          [M, M, M, M, e, e, e, e, e, e, e, e, R, e, e, e, e, e, R, e, e, e, e, e, M,], #16
          [M, M, M, M, e, e, e, e, e, e, e, e, e, e, e, e, e, e, e, R, e, e, e, M, M,], #17
          [M, M, M, e, e, e, e, e, e, e, e, C, M, M, e, e, e, e, e, e, e, e, e, e, M,], #18
          [M, M, M, e, e, e, e, e, e, e, e, e, M, M, e, e, e, e, e, e, e, e, e, e, M,], #19
          [M, M, M, e, e, e, e, e, e, X, e, e, e, e, e, R, e, e, e, e, e, e, e, e, M,], #20
          [M, M, e, e, e, e, e, e, e, e, e, e, e, e, e, e, e, e, e, e, e, e, e, e, M,], #21
          [M, M, X, e, e, M, e, e, e, e, e, e, e, e, e, e, e, e, e, e, e, M, M, M, M,], #22
          [M, M, M, M, M, M, M, e, e, e, e, e, M, M, M, M, e, e, e, e, M, M, M, M, M,], #23
          [M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M,]] #24

# Constants
DEBUG = False
running = True

# Battle Constants
HP_BASE_MOD  = 50
HP_MULT      = 4.5
LUCK_MOD     = 4.0
MISS_BASE    = 10
MISS_MOD     = 1
REROLL_MOD   = .85
WPN_STAT_MOD = 800.0

# Enemy Attr
enemy = {}
enemy["vit"] = 10
enemy["str"] = 10
enemy["lck"] = 9
enemy["wpn"] = 0
enemy["arm"] = 0

#  Game Functions
def debug(s):
    if DEBUG:
        print ('[DEBUG]: %s' % s)

def calcHP(vit): # Used internally by battle() only!
    return ( vit * ( HP_BASE_MOD + ( vit * HP_MULT )))

def attack(atk, dfn, dfnHP): # Used internally by battle() only!
    global enemyHP
    global playerHP
    # Calculate miss or hit. Reroll if mid-range hit
    missChance   = atk["str"] * ((MISS_BASE - (atk["lck"] * 1.5 / 4)) / 100) * MISS_MOD
    rerollWindow = atk["str"] * REROLL_MOD
    goodValue = False
    while goodValue == False:
        rnd = random.random()
        damage = rnd * atk["str"]

        if damage <= missChance:
            damage = 0 # missed!
            goodValue = True
        elif damage > rerollWindow:
            goodValue = True

    if damage != 0:
        damage = (damage + (atk["lck"] / LUCK_MOD)) * atk["str"]
    debug("Base damage is %.3f" % (damage))

    # Weapon mod
    if damage != 0:
        damage += damage * (atk["wpn"] / WPN_STAT_MOD)
    debug("Damage after wpn is %.3f" % (damage))

    #Armor mod
    if damage != 0:
        damage -= damage * (dfn["arm"] / WPN_STAT_MOD)
    debug("Final damage output is %.3f" % (damage))

    return dfnHP - damage

def battle(enemy):
    global running
    player = playerAttr["stat"]
    enemyHP = calcHP(enemy["vit"])
    playerHP = player["HP"]

    con.clear_screen()

    print ("+-------------------------------------------------------------------------+")
    print ("|  Actions:   |  Attack  |  Defend  | *Use Item  | *flee  | * Not avail.  |" )
    print ("|             |          |          |            |        | in current    |")
    print ("|             |   atk    |    def   |     *i     |   *r   | demo version  |" )
    print ('+-------------------------------------------------------------------------+')

    action = input(" You have encountered an evil beast!\nHow do you choose to proceed?\n>>> ")
    if action == "atk": # Player attempts to attack first
        if player["lck"] >= enemy["lck"]:
            print ("\n You react quickly, striking the enemy first!")
            enemyHP = attack(player, enemy, enemyHP)
        else:
            print ("\n You make an attempt at the beast, but he dodges\n your attack and swiftly retaliates.")
            playerHP = attack(enemy, player, playerHP) * 1.2
    elif action == "def": # Player attempt to defend first
        if player["lck"] >= enemy["lck"]:
            print ("\n You block the enemy's initial attack successfully!")
            playerHP = attack(enemy, player, playerHP) / 3.8
        else:
            print ("\n You try to block, but the enemy sidesteps with a\n vicious blow to your side.")
            playerHP = attack(enemy, player, playerHP) * 0.8

    dead = False
    while not dead:

        print (" Player HP: %.2f" % (playerHP))
        print (" Enemy HP:  %.2f" % (enemyHP))

        print ("\n\n")
        debug("Player vs. Enemy:")
        enemyHP = attack(player, enemy, enemyHP)
        if enemyHP <= 0:
            global terMap
            dead = True
            enemyHP = 0
            terMap[playerAttr["pos"][1]][playerAttr["pos"][0]] = e
            #con.clear_screen()
            playerAttr["stat"]["HP"] = playerHP
            print ("You kick the goblin in the face.")
            print ("He died. Oops.")
            input("Press Enter to Continue")
            time.sleep(1)

        print ("\n\n")
        debug("Goblin vs. Player:")
        playerHP = attack(enemy, player, playerHP)
        if playerHP <= 0:
            dead = True
            playerHP = 0
            con.clear_screen()
            print ("\nOh dear! You have died!\n")
            running = False
            input("Press Enter to Return to Main Menu...")
        time.sleep(1)

def spawnPlayer():
    global playerAttr

    playerPosx = playerAttr['pos'][0]
    playerPosy = playerAttr['pos'][1]

    # Place Character on map
    playerSeed = random.randint(1,3)
    if playerSeed == 1:
        playerPosx = 5
        playerPosy = 7
    elif playerSeed == 2:
        playerPosx = 5
        playerPosy = 20
    else:
        playerPosx = 21
        playerPosy = 21

    playerAttr['pos'][0] = playerPosx
    playerAttr['pos'][1] = playerPosy

def terrain():
    global playerPosy, playerPosx

    # Draw map
    print ('')
    for y in range(len(terMap)):
        sys.stdout.write("\t     ")
        for x in range(len(terMap[y])):
            currentChar = terMap[y][x]
            if playerAttr['pos'][0] == x and playerAttr['pos'][1] == y:
                out = unicode(P+" ")
            elif currentChar == H or currentChar == L or currentChar == F:
                out = unicode(currentChar)+H
            elif currentChar == D:
                out = "\b"+(unicode("-")*3)
            else:
                out = unicode(currentChar)+u" "
            sys.stdout.write(out)
        print ('')

directionMap = {'w': [0,-1],'s':[0,1],'a':[-1,0],'d':[1,0]}

def change_direction(pos, direction):
    return [pos[i]+direction[i] for i in xrange(len(pos))]

def is_collision(pos, items):
    posX = pos[0]
    posY = pos[1]
    if terMap[posY][posX] in items:
        return True
    else:
        return False

def moveChar():
    global playerAttr
    char = con.input_char(1)

    playerPos = playerAttr['pos']

    try:
        newPos = change_direction(playerAttr['pos'], directionMap[char])
        if not is_collision(newPos, obsticles):
            playerPos = newPos
        else:
            print ("Can't walk that direction!")

    except KeyError:
        pass

    playerAttr['pos'] = playerPos

def skillAlc():
    vitality     = playerAttr["stat"]["vit"]
    endurance    = playerAttr["stat"]["end"]
    intellegence = playerAttr["stat"]["int"]
    strength     = playerAttr["stat"]["str"]
    dexterity    = playerAttr["stat"]["dex"]
    magika       = playerAttr["stat"]["mag"]
    faith        = playerAttr["stat"]["fth"]
    luck         = playerAttr["stat"]["lck"]

    print ("""

            Character Creation
        This is were you can give your 
        character a name and allocate 
        any skill points you have. You
        start with 10 free points to 
        spend in any skill you see fit.
        """)
    points = 10
    name   = " "
    attrs  = ("1", "2", 
              "3", "4",
              "5", "6",
              "7", "8")
    charMenu = True
    while charMenu:
        print ("""
        Character Name: %s\n
        Vitality ...... %d
        Intellegence .. %d
        Endurance ..... %d
        Strength ...... %d
        Dexterity ..... %d
        Magika ........ %d
        Faith ......... %d
        Luck .......... %d
        """) % (name, vitality, endurance, 
                intellegence, strength, 
                dexterity, magika, faith, luck)
        print (""""\n\n
                1. Name Your Character
                2. Spend Skill Points
                3. Remove Skill Points
                4. Start your adventure
                \n\n""")
        choice = raw_input(" >>> ")
        choosingName = True
        while choosingName:
            if choice == "1":
                print ("\nPlease input a name for your chaacter.")
                name = raw_input("\n Name: ")
                check = raw_input("Are you sure this correct name. y/n\n >>> ")
                if check.lower() == "y":
                    choosingName = False
                else:
                    pass
            elif choice == "2":
                attribute = raw_input("""
        Which Attribute?
        1. Vitality
        2. Intellegence
        3. Endurance
        4. Strength
        5. Dexterity
        6. Magika
        7. Faith
        8. Luck
        9. Back
 >>> """)
                if attribute in attrs:
                    add = int(raw_input(" How many points do you wish to allicate?\n >>> "))
                    if add <= points and add > 0:
                        if attribute == "1":
                            vitality += add
                            print " %s now has %s points in vitality." % (name, vitality)
                            raw_input(" Press Enter to go back to menu.")
                        elif attribute == "2":
                            intellegence += add
                            print " %s now has %s points in intellegence." % (name, intellegence)
                            raw_input(" Press Enter to go back to menu.")
                        elif attribute == "3":
                            endurance += add
                            print " %s now has %s points in endurance." % (name, endurance)
                            raw_input(" Press Enter to go back to menu.")
                        elif attribute == "4":
                            strength += add
                            print " %s now has %s points in strength." % (name, strength)
                            raw_input(" Press Enter to go back to menu.")
                        elif attribute == "5":
                            dexterity += add
                            print " %s now has %s points in dexterity." % (name, dexterity)
                            raw_input(" Press Enter to go back to menu.")
                        elif attribute == "6":
                            magika += add
                            print " %s now has %s points in magika." % (name, magika)
                            raw_input(" Press Enter to go back to menu.")
                        elif attribute == "7":
                            faith += add
                            print " %s now has %s points in faith." % (name, faith)
                            raw_input(" Press Enter to go back to menu.")
                        elif attribute == "8":
                            luck += add
                            print " %s now has %s points in luck." % (name, luck)
                            raw_input(" Press Enter to go back to menu.")
                        point =- add
                    else:
                        print (" ERROR: Please input a valid number.")
                        raw_input(" Press Enter to go back to menu.")
                elif attribute == "9":
                    break
                else:
                    print " ERROR: Please inout a attribute."
                    raw_input(" Press Enter to go back to menu.")
            elif choice == "3":
                attribute = raw_input("""
        Which Attribute?
        1. Vitality
        2. Intellegence
        3. Endurance
        4. Strength
        5. Dexterity
        6. Magika
        7. Faith
        8. Luck
        9. Back
 >>> """)
                if attribute in attrs:
                    take = int(raw_input(" How many points do you wish to allicate?\n >>> "))
                    if take <= points and add > 0:
                        if attribute == "1":
                            vitality -= take
                            print " %s now has %s points in vitality." % (name, vitality)
                            points += take
                            raw_input(" Press Enter to go back to menu.")
                        elif attribute == "2":
                            intellegence -= take
                            print " %s now has %s points in intellegence." % (name, intellegence)
                            points += take
                            raw_input(" Press Enter to go back to menu.")
                        elif attribute == "3":
                            endurance -= take
                            print " %s now has %s points in endurance." % (name, endurance)
                            points += take
                            raw_input(" Press Enter to go back to menu.")
                        elif attribute == "4":
                            strength -= take
                            print " %s now has %s points in strength." % (name, strength)
                            points += take
                            raw_input(" Press Enter to go back to menu.")
                        elif attribute == "5":
                            dexterity -= take
                            print " %s now has %s points in dexterity." % (name, dexterity)
                            points += take
                            raw_input(" Press Enter to go back to menu.")
                        elif attribute == "6":
                            magika -= take
                            print " %s now has %s points in magika." % (name, magika)
                            points += take
                            raw_input(" Press Enter to go back to menu.")
                        elif attribute == "7":
                            faith -= take
                            print " %s now has %s points in faith." % (name, faith)
                            points += take
                            raw_input(" Press Enter to go back to menu.")
                        elif attribute == "8":
                            luck -= take
                            print " %s now has %s points in luck." % (name, luck)
                            points += take
                            raw_input(" Press Enter to go back to menu.")
                    else:
                        print (" ERROR: Please input a valid number.")
                        raw_input(" Press Enter to go back to menu.")
                elif attribute == "9":
                    break
                else:
                    print " ERROR: Please inout a attribute."
                    raw_input(" Press Enter to go back to menu.")
            elif choice == "4":
                print" Adventure starting in 3 secs."
                time.sleep(1)
                print" Adventure starting in 2 secs."
                time.sleep(1)
                print" Adventure starting in 1 sec."
                time.sleep(1)
                choosingName = False
                charMenu = False

    playerAttr["stat"]["vit"] = vitality    
    playerAttr["stat"]["end"] = endurance   
    playerAttr["stat"]["int"] = intellegence
    playerAttr["stat"]["str"] = strength    
    playerAttr["stat"]["dex"] = dexterity   
    playerAttr["stat"]["mag"] = magika      
    playerAttr["stat"]["fth"] = faith       
    playerAttr["stat"]["lck"] = luck        

def charSelect():
    valid = False
    while not valid:
        con.clear_screen()
        print (" Please input the name of the class you wish to be.")
        print (" 1. Warrior")
        print (" 2. Knight")
        print (" 3. Royalty")
        print (" 4. Mage")
        print (" 5. Thief")
        print (" 6. Hunter")

        charClass = input('\n>>> ')
        # data validation
        if charClass.lower() in ("warrior", "1"):
            warriorAttr()
            valid = True
        elif charClass.lower() in ("knight", "2"):
            knightAttr()
            valid = True
        elif charClass.lower() in ("royalty", "3"):
            royaltyAttr()
            valid = True
        elif charClass.lower() in ("mage", "4"):
            mageAttr()
            valid = True
        elif charClass.lower() in ("thief", "5"):
            thiefAttr()
            valid = True
        elif charClass.lower() in ("hunter", "6"):
            hunterAttr()
            valid = True

    playerAttr["stat"]["HP"] = calcHP(playerAttr["stat"]["vit"])
    skillAlc()

def playGame():
    global playerAttr, running

    spawnPlayer()
    while running:

        playerHP = playerAttr["stat"]["HP"]
        vitality = playerAttr["stat"]["vit"]
        strength = playerAttr["stat"]["str"]
        luck     = playerAttr["stat"]["lck"]
        weapon   = playerAttr["stat"]["wpn"]
        armor    = playerAttr["stat"]["arm"]
        con.clear_screen()
        print ("+-------------------------------------------------------------------------+")
        print ("|  Player HP : {:<8.1f}                                                   |".format(playerHP))
        print ("|  Stats:   |  Vitality  |  Strength  |  Luck  |  Weapon  |  Armor  |     |")
        print ("|           |     %s     |     %s     |   %s    |    %s    |    %s   |     |" % (vitality, strength, luck, weapon, armor))
        print ('+-------------------------------------------------------------------------+')
        terrain()
        print ('')
        print ('+-------------------------------------------------------------------------+')
        print ("| Legend:   |  Mountain  |  Goblin  |  Chest  |  Pepper Chest  |  Player  |")
        print ("|           |     %s      |     %s    |    %s    |        %s       |     %s    |" % (M, G, C, X, P))
        print ('+-------------------------------------------------------------------------+')
        print ("| Controls: |     North     |     South     |     East     |     West     |")
        print ("|           |       W       |       A       |       S      |      D       |")
        print ('+-------------------------------------------------------------------------+')
        moveChar()
        playerPosy = playerAttr['pos'][1]
        playerPosx = playerAttr['pos'][0]
        if terMap[playerPosy][playerPosx] == D:
            con.clear_screen()
            print ("\n\n    YOU IS WIN!1!!1!")
            print ('')
            input(" Press enter to return to main menu.")
            running = False
        elif terMap[playerPosy][playerPosx] in [R,G,X]:
            battle(enemy)

def menu():
    global running
    while True:
        con.clear_screen()
        print ("\n\n\t\tAdventures of Grogg?")
        print ("\n\tWelcome to the greatest texted based ")
        print ("\tadventure you have ever played.\n\n")
        print (" Start\n Exit\n")
        x = input('\n>>> ')
        con.clear_screen()
        if x.lower() == "start":
            running = True
            charSelect()
            playGame()
        elif x.lower() == "exit":
            print ("\nExiting\n")
            con.clear_color()
            con.clear_screen()
            break
        else:
            print ("\n\n\aERROR: NOT A VALID INPUT\n")

if __name__ == "__main__":
    menu()
