import os
import platform
import random
import sys
import time

os.system("color 02")

PYTHON_3 = sys.version_info.major == 3

if PYTHON_3:
    range = range
    unicode = str
    input = input
else:
    range = xrange
    unicode = unicode
    input = raw_input

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

# Battle Constants
HP_BASE_MOD  = 50
HP_MULT      = 4.5
LUCK_MOD     = 4.0
MISS_BASE    = 10
MISS_MOD     = 1
REROLL_MOD   = .85
WPN_STAT_MOD = 800.0

# Player information
playerAttr = {}

running = True

# Enemy Attr
enemy = {}
enemy["vit"] = 10
enemy["str"] = 10
enemy["lck"] = 9
enemy["wpn"] = 0
enemy["arm"] = 0

# Character Attr Functions
#warriorAttr["stat"]["lck"]
def warriorAttr():
    playerAttr["role"] = "Warrior"
    playerAttr["posx"] = 0
    playerAttr["posy"] = 0
    playerAttr["stat"] = {}
    playerAttr["stat"]["HP"] = 0
    playerAttr["stat"]["vit"] = 14
    #playerAttr["stat"]["int"] = 9
    #playerAttr["stat"]["end"] = 12
    playerAttr["stat"]["str"] = 12
    #playerAttr["stat"]["dex"] = 11
    #playerAttr["stat"]["mag"] = 8
    #playerAttr["stat"]["fth"] = 10
    playerAttr["stat"]["lck"] = 7
    playerAttr["stat"]["wpn"] = 40
    playerAttr["stat"]["arm"] = 35

def knightAttr():
    playerAttr["role"] = "Knight"
    playerAttr["posx"] = 0
    playerAttr["posy"] = 0
    playerAttr["stat"] = {}
    playerAttr["stat"]["HP"] = 0
    playerAttr["stat"]["vit"] = 10
    #playerAttr["stat"]["int"] = 11
    #playerAttr["stat"]["end"] = 11
    playerAttr["stat"]["str"] = 14
    #playerAttr["stat"]["dex"] = 10
    #playerAttr["stat"]["mag"] = 10
    #playerAttr["stat"]["fth"] = 11
    playerAttr["stat"]["lck"] = 10
    playerAttr["stat"]["wpn"] = 35
    playerAttr["stat"]["arm"] = 40

def royaltyAttr():
    playerAttr["role"] = "Royalty"
    playerAttr["posx"] = 0
    playerAttr["posy"] = 0
    playerAttr["stat"] = {}
    playerAttr["stat"]["HP"] = 0
    playerAttr["stat"]["vit"] = 8
    #playerAttr["stat"]["int"] = 12
    #playerAttr["stat"]["end"] = 8
    playerAttr["stat"]["str"] = 9
    #playerAttr["stat"]["dex"] = 12
    #playerAttr["stat"]["mag"] = 13
    #playerAttr["stat"]["fth"] = 12
    playerAttr["stat"]["lck"] = 7
    playerAttr["stat"]["wpn"] = 30
    playerAttr["stat"]["arm"] = 15

def mageAttr():
    playerAttr["role"] = "Mage"
    playerAttr["posx"] = 0
    playerAttr["posy"] = 0
    playerAttr["stat"] = {}
    playerAttr["stat"]["HP"] = 0
    playerAttr["stat"]["vit"] = 9
    #playerAttr["stat"]["int"] = 15
    #playerAttr["stat"]["end"] = 10
    playerAttr["stat"]["str"] = 9
    #playerAttr["stat"]["dex"] = 11
    #playerAttr["stat"]["mag"] = 15
    #playerAttr["stat"]["fth"] = 6
    playerAttr["stat"]["lck"] = 11
    playerAttr["stat"]["wpn"] = 32
    playerAttr["stat"]["arm"] = 20

def thiefAttr():
    playerAttr["role"] = "thief"
    playerAttr["posx"] = 0
    playerAttr["posy"] = 0
    playerAttr["stat"] = {}
    playerAttr["stat"]["HP"] = 0
    playerAttr["stat"]["vit"] = 10
    #playerAttr["stat"]["int"] = 13
    #playerAttr["stat"]["end"] = 10
    playerAttr["stat"]["str"] = 9
    #playerAttr["stat"]["dex"] = 14
    #playerAttr["stat"]["mag"] = 10
    #playerAttr["stat"]["fth"] = 8
    playerAttr["stat"]["lck"] = 15
    playerAttr["stat"]["wpn"] = 20
    playerAttr["stat"]["arm"] = 25

def hunterAttr():
    playerAttr["role"] = "hunter"
    playerAttr["posx"] = 0
    playerAttr["posy"] = 0
    playerAttr["stat"] = {}
    playerAttr["stat"]["HP"] = 0
    playerAttr["stat"]["vit"] = 12
    #playerAttr["stat"]["int"] = 10
    #playerAttr["stat"]["end"] = 13
    playerAttr["stat"]["str"] = 11
    #playerAttr["stat"]["dex"] = 12
    #playerAttr["stat"]["mag"] = 8
    #playerAttr["stat"]["fth"] = 8
    playerAttr["stat"]["lck"] = 12
    playerAttr["stat"]["wpn"] = 45
    playerAttr["stat"]["arm"] = 15

#  Game Functions

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
    # ( print "[DEBUG] Base damage is %.3f" % (damage))
    
    # Weapon mod
    if damage != 0:
        damage += damage * (atk["wpn"] / WPN_STAT_MOD)
    # ( print "[DEBUG] Damage after wpn is %.3f" % (damage))
    
    #Armor mod
    if damage != 0:
        damage -= damage * (dfn["arm"] / WPN_STAT_MOD)
    # ( print "[DEBUG] Final damage output is %.3f" % (damage))
    
    return dfnHP - damage

def battle(enemy):
    global running
    player = playerAttr["stat"]
    enemyHP = calcHP(enemy["vit"])
    playerHP = player["HP"]

    clear()

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
        #print ("[DEBUG] Player vs. Enemy:")
        enemyHP = attack(player, enemy, enemyHP)
        if enemyHP <= 0:
            global terMap
            dead = True
            enemyHP = 0
            terMap[playerAttr["posy"]][playerAttr["posx"]] = e
            #clear()
            playerAttr["stat"]["HP"] = playerHP
            print ("You kick the goblin in the face.")
            print ("He died. Oops.")
            input("Press Enter to Continue")
            time.sleep(1)
        
        print ("\n\n")
        #print ("[DEBUG] Goblin vs. Player:")
        playerHP = attack(enemy, player, playerHP)
        if playerHP <= 0:
            dead = True
            playerHP = 0
            clear()
            print ("\nOh dear! You have died!\n")
            running = False
            input("Press Enter to Return to Main Menu...")
        time.sleep(1)

def spawnPlayer():
    global playerAttr

    playerPosx = playerAttr['posx']
    playerPosy = playerAttr['posy']

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

    playerAttr['posx'] = playerPosx
    playerAttr['posy'] = playerPosy

def terrain():
    global playerPosy, playerPosx
    
    # Draw map
    print ()
    for y in range(len(terMap)):
        sys.stdout.write("\t     ")
        for x in range(len(terMap[y])):
            #print ( x, y)
            currentChar = terMap[y][x]
            if playerAttr['posx'] == x and playerAttr['posy'] == y:
                out = unicode(P+" ")
            elif currentChar == H or currentChar == L or currentChar == F:
                out = unicode(currentChar)+H
            elif currentChar == D:
                out = "\b"+(unicode("-")*3)
            else:
                out = unicode(currentChar)+u" "
            sys.stdout.write(out)
        print ()

def moveChar():
    global playerAttr
    direction = input("    Move direction: ")

    playerPosy = playerAttr['posy']
    playerPosx = playerAttr['posx']

    if direction == "w":
        if terMap[playerPosy-1][playerPosx] in obsticles:
            print ("Can't walk that direction!")
        else:
            playerPosy -= 1

    elif direction == "s":
        if terMap[playerPosy+1][playerPosx] in obsticles:
            print ("Can't walk that direction!")
        else:
            playerPosy += 1

    elif direction == "a":
        if terMap[playerPosy][playerPosx-1] in obsticles:
            print ("Can't walk that direction!")
        else:
            playerPosx -= 1

    elif direction == "d":
        if terMap[playerPosy][playerPosx+1] in obsticles:
            print ("Can't walk that direction!")
        else:
            playerPosx += 1

    playerAttr['posx'] = playerPosx
    playerAttr['posy'] = playerPosy

def skillAlc():
    vitality = playerAttr["stat"]["vit"]
    strength = playerAttr["stat"]["str"]
    luck     = playerAttr["stat"]["lck"]
    clear()
    print ("\n\n        Character Creation")
    print ("\n\n    Welcome to the character creator.")
    print ("    Here you can edit your character by ")
    print ("    adding any points that you have to ")
    print ("    varius stats.\n")
    name=input("    What's your character's name? ")
    points=10
    attributes=("vitality", "strength", "luck")

    while True:
        clear()
        print ()
        print (" you have %s points left." % (points))
        print ("""
        1-spend skill points
        2-remove skill points
        3-view skill points
        4-done
        """)
        choice = input("    choice: ")
        clear()
        if choice == "1":
            attribute = input(" which attribute? \n 1. strength\n 2. vitality\n 3. luck\n >>> ")
            if attribute in attributes:
                add = int(input(" how many points? "))
                if add <= points and add > 0:
                    if attribute == "strength" or attribute == "1":
                        strength += add
                        print (" %s now has %s points in strength." % (name, strength))
                        input(" Press Enter to go back to menu.")
                        clear()
                    elif attribute == "vitality" or attribute == "2":
                        vitality += add
                        print (" %s now has %s points in vitality." % (name, vitality))
                        input(" Press Enter to go back to menu.")
                        clear()
                    elif attribute == "luck" or attribute == "3":
                        luck += add
                        print (" %s now has %s points in luck." % (name, luck))
                        input(" Press Enter to go back to menu.")
                        clear()
                    points -= add
                else:
                    print (" invalid number of points.")
                    input(" Press Enter to go back to menu.")
                    clear()
            else:
                print (" invalid attribute.")
                input(" Press Enter to go back to menu.")
                clear()
        elif choice == "2":
            attribute = input("\n which attribute? strength, vitality, or luck? ")
            if attribute in attributes:
                take = int(input("\n how many points? "))
                if attribute == "1" and take <= strength and take > 0:
                    strength -= take
                    print (" %s now has %s points in strength." % (name, strength))
                    points += take
                    input(" Press Enter to go back to menu.")
                    clear()
                elif attribute == "2" and take <= vitality and take > 0:
                    vitality -= take
                    print (" %s now has %s points in vitality." % (name, vitality))
                    points += take
                    input(" Press Enter to go back to menu.")
                    clear()
                elif attribute == "3" and take <= dexterity and take > 0:
                    luck -= take
                    print (" %s now has %s points in luck." % (name, luck))
                    points += take
                    input(" Press Enter to go back to menu.")
                    clear()
                else:
                    print (" invalid number of points.")
                    input(" Press Enter to go back to menu.")
                    clear()
            else:
                print (" invalid attribute.")
                input(" Press Enter to go back to menu.")
                clear()
        elif choice == "3":
            print ("  strength - %s" % strength)
            print ("  vitality - %s" % vitality)
            print ("  luck - %s" % luck)
            input(" Press Enter to go back to menu.")
            clear()
        elif choice == "4":
            if points == 0:
                print ("\n congrats! you're done designing %s." % (name))
                print (" %s has %s strength, %s vitality, and %s luck." % (name, strength, vitality, luck))
                input(" Press Enter to start your adventure.")
                clear()
                break
            else:
                print (" use all your points!")
                input(" Press Enter to go back to menu.")
                clear()
        else:
            print (" invalid choice.")
            input(" Press Enter to go back to menu.")
            clear()

    playGame()

    playerAttr["stat"]["vit"] = vitality
    playerAttr["stat"]["str"] = strength
    playerAttr["stat"]["lck"] = luck

def charSelect():
    valid = False
    while not valid:
        clear()
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

def clear():
    if platform.system() == 'Windows':
        clearCmd = 'cls'
    else: # *nix
        clearCmd = 'clear'
    os.system(clearCmd)

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
        clear()
        print ("+-------------------------------------------------------------------------+")
        print ("|  Player HP : {:<8.1f}                                                   |".format(playerHP))
        print ("|  Stats:   |  Vitality  |  Strength  |  Luck  |  Weapon  |  Armor  |     |")
        print ("|           |     %s     |     %s     |   %s    |    %s    |    %s   |     |" % (vitality, strength, luck, weapon, armor))
        print ('+-------------------------------------------------------------------------+')
        terrain()
        print ()
        print ('+-------------------------------------------------------------------------+')
        print ("| Legend:   |  Mountain  |  Goblin  |  Chest  |  Pepper Chest  |  Player  |")
        print ("|           |     %s      |     %s    |    %s    |        %s       |     %s    |" % (M, G, C, X, P))
        print ('+-------------------------------------------------------------------------+')
        print ("| Controls: |     North     |     South     |     East     |     West     |")
        print ("|           |       W       |       A       |       S      |      D       |")
        print ('+-------------------------------------------------------------------------+')
        moveChar()
        playerPosy = playerAttr['posy']
        playerPosx = playerAttr['posx']
        if terMap[playerPosy][playerPosx] == D:
            clear()
            print ("\n\n    YOU IS WIN!1!!1!")
            print ()
            input(" Press enter to return to main menu.")
            running = False
        elif terMap[playerPosy][playerPosx] in [R,G,X]:
            battle(enemy)
            
def menu():
    global running
    while True:

        clear()
        print ("\n\n\t\tAdventures of Grogg?")
        print ("\n\tWelcome to the greatest texted based ")
        print ("\tadventure you have ever played.\n\n")
        print (" Start\n Exit\n")
        x = input('\n>>> ')
        clear()
        if x.lower() == "start":
            running = True
            charSelect()
            playGame()
        elif x.lower() == "exit":
            print ("\nExiting\n")
            os.system("color 56")
            break
        else:
            print ("\n\n\aERROR: NOT A VALID INPUT\n")

if __name__ == "__main__":
    menu()
