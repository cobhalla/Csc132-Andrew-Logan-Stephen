#################################################################################
# Adrew Hall
# a basic game as proof of concept for integrating tkinter and GPIO
#################################################################################
'''
necicary gifs:
"Gangsta.gif"
"Goblin.gif"
"RedGoblin.gif"
"EggPyre.gif"
'''
##############
# Imports
##############

# abstract classes
import abc
# random numbers
from random import randint
# GUI
from Tkinter import *
# Physical I/O w/ breadboard
#import RPi.GPIO as GPIO
# Timers
from time import sleep

##############
#GPIO setup
##############
# tactile mon=mentary switches
# button R B Y G
#buttons = [26, 12, 16, 20]
# physical response
# led R B Y G
#leds = [6, 13, 19, 21]

#GPIO.setmode(GPIO.BCM)

#GPIO.setup(leds, GPIO.OUT)
#GPIO.setup(buttons, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

##############
# GPIO Test
##############
##def test():
##  for i in range(len(leds)):
##    GPIO.output(leds[i], True)
##    sleep(1)
##    GPIO.output(leds[i], False)
##    sleep(0.5)
##  print "Sionara!"
##  GPIO.cleanup()

##############
# Classes
##############
class Being(object):
    __metaclass__ = abc.ABCMeta
    def __init__(self, name, health, atk, defn):
        self.name = name
        self.maxHP = health
        self.health = health
        self.atk = atk
        self.defn = defn

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, value):
        if value >= self.maxHP:
            self._health = self.maxHP
        if value <= 0:
            self._health = 0
        else:
            self._health = value

    @property
    def atk(self):
        return self._atk

    @atk.setter
    def atk(self, value):
        if(value < 0):
            self._atk = 0
        else:
            self._atk = value

    @property
    def defn(self):
        return self._defn
            
    @defn.setter
    def defn(self, value):
        if(value < 0):
            self._defn = 0
        else:
            self._defn = value

    def __str__(self):
        return "{}.\n {}/{} Health, {} Attack, {} Defence".format(\
            self.name, self.health, self.maxHP, self.atk, self.defn)

class Monster(Being):
    __metaclass__ = abc.ABCMeta
    def __init__(self, name, health, atk, defn, image):
        Being.__init__(self, name, health, atk, defn)
        self.image = image
        self.coins = 1
        self.loot = "old boots"
        self.setLoot()

    

    @abc.abstractmethod
    def setLoot(Self):
        """This is where you put the drop table for each monster """
        

class Goblin(Monster):
    def __init__(self):
        Monster.__init__(self, "Goblin", 10, 4, 1, "Goblin.gif")

    def setLoot(self):
        self.loot = "monster_horn" 

class RedGoblin(Monster):
    def __init__(self):
        Monster.__init__(self, "RedGoblin", 20, 6, 2, "RedGoblin.gif")
        self.coins = 2

    def setLoot(self):
        self.loot = "taters"

class EggPyre(Monster):
    def __init__(self):
        Monster.__init__(self, "EggPyre", 50, 20, 15, "EggPyre.gif")
        self.coins = 10

    def setLoot(self):
        self.loot = "boody fang"

class Gangsta(Monster):
    def __init__(self):
        Monster.__init__(self, "Gangsta", 100, 50, 30, "Gangsta.gif")
        self.coins = 50

    def setLoot(self):
        self.loot = "powder"

        
class Player(Being):
    def __init__(self):
        name = self.getName()        
        Being.__init__(self, name, 100, 3, 3)
        self.maxHP = 100
        self.inventory = {"potion" : 10}
        self.coins = 100
        self.kills = 1

    @property
    def kills(self):
        return self._kills
    
    @kills.setter
    def kills(self, value):
        self._kills = value
        if(self._kills % 10 == 0):
            self.atk += 1
            self.defn += 1
        if(self._kills % 50 == 0):
            self.atk += 4
            self.defn += 4
        if(self._kills % 100 == 0):
            self.atk += 15
            self.defn += 15
        

    def addInventory(self, item):
        keys = self.inventory.keys()
        if item in keys:
            self.inventory[item] += 1
        else:
            self.inventory[item] = 1           
        

    def getName(self):
        #ask the user for a name
        return "jeff"
    
class Game(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

    def firstMonster(self):
        Game.currentMonster = Goblin()

    def randMonster(self):
        rint = randint(0,100)
        if Game.player.kills < 50:
            if rint < 50:
                return Goblin()
            else:
                return RedGoblin()
        if Game.player.kills >= 50 and Game.player.kills < 100:
            if rint < 30:
                return Goblin()
            if(rint >= 30) and (rint <80):
                return RedGoblin()
            if(rint >= 80) and (rint <100):
                return EggPyre()
        if Game.player.kills >= 100:
            if rint < 10:
                return Goblin()
            if(rint >= 10) and (rint <50):
                return RedGoblin()
            if(rint >= 50) and (rint <90):
                return EggPyre()
            if(rint >= 90) and (rint <100):
                return Gangsta()
        

    def setupGUI(self):
        # organize the GUI
        self.pack(fill = BOTH, expand = 1)

        # setup the player input at the bottom of the GUI
        # the widget is a Tkinter Entry
        # set its background to white and bind the return key to the
        # function process in the class
        # push it to the bottom of the Gui and let it fill
        # horizontaly
        # give it focus so the player doesn't have to clikkkk on it
        Game.player_input = Entry(self, bg = "white")
        Game.player_input.bind("<Return>", self.process)
        #Game.player_input.bind("<b>", self.processButton)
        Game.player_input.pack(side = BOTTOM, fill = X)
        Game.player_input.focus()

        # setup the image to the left of the GUI
        # the widget is a Tkinter Label
        # don't let the image control the widget's size
        img = None
        Game.image = Label(self, width = WIDTH / 2, image = img)
        Game.image.image = img
        Game.image.pack(side = LEFT, fill = Y)
        Game.image.pack_propagate(False)

        # setup the text to the right of the GUI
        # first, the frame in which the text will be placed
        text_frame = Frame(self, width = WIDTH / 2)
        # the widget is a Tkinter Text
        # disable it by default
        # dont let the Widget controll the frame's size
        Game.text = Text(text_frame, bg = "lightgrey", state = DISABLED)
        Game.text.pack(fill = Y, expand = 1)
        text_frame.pack(side = RIGHT, fill = Y)
        text_frame.pack_propagate(False)

    def setMonsterImage(self):
        #ripped straight from room adventure
        if (Game.currentMonster == None):
            Game.img = PhotoImage(file = "Smile.gif")
        else:
            Game.img = PhotoImage(file = Game.currentMonster.image)

        Game.image.config(image = Game.img)
        Game.image.image = Game.img

    def setStatus(self, status):
        # enable the text widget, clear it, set it, and disabled it
        Game.text.config(state = NORMAL)
        Game.text.delete("1.0", END)
        if (Game.currentMonster == NONE):
            # if dead, let the player know
            Game.text.insert(END, "YOU DIED! You should just QUIT.\n")
        else:
            # otherwise
            Game.text.insert(END, str(Game.currentMonster) +\
                             "\n" + str(Game.player) +\
                             "\nYou Have {} coins".format(Game.player.coins) +\
                             "\nYou are carrying: " + str(Game.player.inventory) +\
                             "\n\n" + status)
            Game.text.config(state = DISABLED)
        

    def play(self):
        Game.player = Player()
        self.firstMonster()
        self.setupGUI()
        self.setMonsterImage()
        self.setStatus("")

##    def processButton(self):
##        pressed = False
##        # as long as no switch is pressed
##        while(not pressed):
##            # check status of each switch
##            for i in range(len(buttons)):
##                # if a button is pressed
##                while(GPIO.input(buttons[i]) == True):
##                    # track which one is pressed
##                    # val is the index in buttons
##                    # not the value of the pin
##                    val = i
##                    pressed = True
##        if(val == 0):
##            self.process("attack")
##            GPIO.output(leds[val], True)
##            sleep(1)
##            GPIO.output(leds[val], False)
##        if(val == 1):
##            self.process("use potion")
##            GPIO.output(leds[val], True)
##            sleep(1)
##            GPIO.output(leds[val], False)
##        if(val == 2):
##            self.process("buy sword")
##            GPIO.output(leds[val], True)
##            sleep(1)
##            GPIO.output(leds[val], False)
##        if(val == 3):
##            self.process("buy shield")
##            GPIO.output(leds[val], True)
##            sleep(1)
##            GPIO.output(leds[val], False)
        
            
        

    def process(self, event):
        # grab the player's input from the input at the bottom of
        # the GUI
        action = Game.player_input.get()
        # set the user's input to lowercase to make it easier to compare
        # the verb and noun to known values
        action = action.lower()
        # set a default response
        response = "I don't understand. Try verb noun.\
                    Valid verbs are: attack, shop, use"
        # exit the game if the player wants to leave (supports quit,
        if (action == "quit" or action == "exit" or action == "bye"\
            or action == "sionara!"):
            exit(0)

        # if the player is dead
        if((Game.currentMonster == None) or (Game.player.health <= 0)):
            # clear the player's input
            Game.player_input.delete(0, END)
            return
        
        # split the user input into words (words are separated
        # by spaces) and store the words as a list
        words = action.split()

        if(len(words) == 1):
            verb = words[0]
            
            # You atack the monster
            if(verb == "attack"):
                skipATK = False
                yourAtk = Game.player.atk
                monsterDefn = Game.currentMonster.defn
                #if your atk lvl is higher then the monsters defence
                if(yourAtk >= monsterDefn):
                    #You hit for your atk - the mondters defense
                    hpLoss = yourAtk - monsterDefn
                    #the monster looses hp
                    Game.currentMonster.health -= hpLoss
                    response = "you hit for {} hp".format(hpLoss)
                    #if your atk puts the monster @ or below 0 hp
                    if(Game.currentMonster.health <= 0):
                        skipATK = True
                        response = "You kill the monster"
                        #give the player loot
                        Game.player.coins += self.currentMonster.coins
                        Game.player.kills += 1
                        Game.player.addInventory(Game.currentMonster.loot)
                        #genorate the new monster
                        newMonster = self.randMonster()
                        Game.currentMonster = newMonster     
                else:
                    response = "your attack does nothing"
                #if you do not kill the monster it will attack you
                if skipATK == False:
                    monsterAtk = Game.currentMonster.atk
                    playerDefn = Game.player.defn
                    if (monsterAtk >= playerDefn):
                        hpLoss = monsterAtk - playerDefn
                        Game.player.health -= hpLoss
            if(verb == "shop"):
                response = "Shop Items: " +\
                           "\npotion: +20 HP 10 coins" +\
                           "\nsword: +1 atk 20 coins" +\
                           "\nshield: +1 defn 20 coins " 
                           
            
        if(len(words) == 2):
            verb = words[0]
            noun1 = words[1]

            if(verb == "buy"):
                response = "Yuo dont have enough money"
                if(noun1 == "potion"):
                    if(Game.player.coins >= 10):
                        Game.player.coins -= 10
                        Game.player.addInventory("potion")
                        response = "You buy a potion"
                if(noun1 == "sword"):
                    if(Game.player.coins >= 20):
                        Game.player.coins -= 20
                        Game.player.atk += 1
                        response = "You buy a better sword"
                if(noun1 == "shield"):
                    if(Game.player.coins >= 20):
                        Game.player.coins -= 20
                        Game.player.defn += 1
                        response = "You buy a better shield"
            #consume items
            if(verb == "use"):
                response = "You can't do that right now"
                if(noun1 == "taters"):
                    #default the player doesnt have a taters
                    response = "You dont have any"
                    #the player has some taters
                    #the player can always use taters even at maxHP
                    if(Game.player.inventory["taters"] >= 1):
                        #increase maxHP
                        Game.player.maxHP += 10
                        #remove a taters
                        Game.player.inventory["taters"] -= 1
                        response = "You feel better"
                        
                if(noun1 == "potion"):
                    #default the player doesnt have a potion
                    response = "You dont have any"
                    #the player has a potion
                    if(Game.player.inventory["potion"] >= 1):
                        response = "You dont need to do that yet"
                        #the porion will heal you AT LEAST 10/20 points
                        if(Game.player.health + 10 <= Game.player.maxHP):
                            Game.player.health += 20
                            Game.player.inventory["potion"] -= 1
                            response = "You drink a potion"
                            
                if(noun1 == "monster_horn"):
                    response = "You dont have enough"
                    #the player has 10 monster horns
                    if(Game.player.inventory["monster_horn"] >= 10):
                      Game.player.inventory["monster_horn"] -= 10
                      Game.player.inventory["horn_dust"] += 1
                      response = "You grind the horns into dust"
                if(noun1 == "horn_dust"):
                  #default the player has no horn dust
                  response = "You dont have any"
                  #does the player have a dust?
                  if(Game.player.inventory["horn_dust"] >= 1):
                    # the player has dust but no potion
                    response = "You dont have a potion to mix it with"
                    # does the player have a potion
                    if(Game.player.inventory["potion"] >= 1):
                      Game.player.inventory["horn_dust"] -= 1
                      Game.player.inventory["potion"] -= 1
                      Game.player.inventory["super_potion"] += 1
                      
                  
                      
                        
                    
        if(len(words) == 3):
##            verb = words[0]
##            noun1 = words[1]
##            noun2 = words[2]
            pass

        # display the response on the right of the GUI
        # display the room's image on the left of the GUI
        # clear the player's input
        self.setStatus(response)
        self.setMonsterImage()
        Game.player_input.delete(0, END)

######################################################################
# the default size of the GUI is 800x600
WIDTH = 800
HEIGHT = 600

#create the window
window = Tk()
window.title("Goblin Slayer")

#create the GUI as Tkinter canvas inside the window
g = Game(window)
#Play the game
g.play()

#wait for the window to close
window.mainloop()





        
    
