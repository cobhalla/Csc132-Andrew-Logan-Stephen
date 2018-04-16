##################################################################################
# Andrew Hall
# basic multi gui test
##################################################################################

#imports
# abstract classes
import abc
# random numbers
from random import randint
# GUI
from Tkinter import *

##########
# Beings
##########
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
    
##########
# GUI
##########
class Manager(Tk):
    def __init__(self, ):
        Tk.__init__(self)
        container = Frame(self)
        container.pack(side = "top", fill = "both", expand = True)
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
        self.player = Player()

        self.frames = {}
        for F in (Game, Pause, Shop):
            page_name = F.__name__
            frame = F(self.player, parent = container, controller = self)
            self.frames[page_name] = frame
            frame.grid(row = 0, column = 0, sticky = "nsew")

        self.show_frame("Game")
        

    def show_frame(self, page_name):
        '''Shows the selected frame'''
        frame = self.frames[page_name]
        frame.tkraise()
        
        

class Game(Frame):
    def __init__(self, player, parent, controller):
        Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller
        Game.player = player
        label = Label(self, text = "Game")
        label.grid(row = 0, column = 0, sticky = NW )
        label1 = Label(self, text = Game.player.name)
        label1.grid(row = 0, column = 1)
        button1 = Button(self, text = "Pause",\
                         command = lambda: controller.show_frame("Pause"))
        button2 = Button(self, text = "Shop",\
                         command = lambda: controller.show_frame("Shop"))
        button3 = Button(self, text = "Attack",\
                         command = self.attack())
        
        button1.grid(row = 1, column = 0, sticky = NW)
        button2.grid(row = 1, column = 1, sticky = NW)
        button3.grid(row = 3, column = 0, sticky = NW)

        Game.currentMonster = Goblin()
        
        img = None
        Game.image = Label(self, width = WIDTH / 2, image = img)
        Game.image.image = img
        Game.image.grid(row = 2, column = 0, columnspan = 2)
##        text_frame = Frame(self, width = WIDTH / 2)
##        Game.text = Text(text_frame, bg = "lightgrey", state = DISABLED)
##        #Game.text.grid(row = 2, column = 4)#, columnspan = 3)
##        Game.text.insert(END, "hello")
        Game.text = "hello"
        Game.textLabel = Label(self, text = Game.text)
        Game.textLabel.grid(row = 2, column = 2, columnspan = 1, sticky = NW)

        self.setMonsterImage()
        #self.setStatus("")

        


    def randMonster(self):
        rint = randint(0,100)
        if self.controller.player.kills < 50:
            if rint < 50:
                return Goblin()
            else:
                return RedGoblin()
        if self.controller.player.kills >= 50 and Game.player.kills < 100:
            if rint < 30:
                return Goblin()
            if(rint >= 30) and (rint <80):
                return RedGoblin()
            if(rint >= 80) and (rint <100):
                return EggPyre()
        if self.controller.player.kills >= 100:
            if rint < 10:
                return Goblin()
            if(rint >= 10) and (rint <50):
                return RedGoblin()
            if(rint >= 50) and (rint <90):
                return EggPyre()
            if(rint >= 90) and (rint <100):
                return Gangsta()
            
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
##        Game.text.config(state = NORMAL)
##        Game.text.delete("1.0", END)
        if (Game.currentMonster == NONE):
            # if dead, let the player know
            Game.text.insert(END, "YOU DIED! You should just QUIT.\n")
        else:
            # otherwise
            Game.text =  str(Game.currentMonster) +\
                             "\n" + str(Game.player) +\
                             "\nYou Have {} coins".format(Game.player.coins) +\
                             "\nYou are carrying: " + str(Game.player.inventory) +\
                             "\n\n" + status
            #Game.text.config(state = DISABLED)
            
    def attack(self):
        pass
        


class Pause(Frame):
    
    def __init__(self, player, parent, controller):
        Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller
        Pause.player = player
        label = Label(self, text = "Pause")
        label.grid(row = 0, column = 0 )
        button1 = Button(self, text = "Game",\
                         command = lambda: controller.show_frame("Game"))
        button2 = Button(self, text = "Shop",\
                         command = lambda: controller.show_frame("Shop"))
        button1.grid(row = 1, column = 0 )
        button2.grid(row = 1, column = 1 )
        


class Shop(Frame):
    
    def __init__(self, player, parent, controller):
        Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller
        Shop.player = player
        Shop.text = ""
        label1 = Label(self, text = "welcome to the Shop")
        label2 = Label(self, text = "You have {} coins.".format(Shop.player.coins))
        label3 = Label(self, text = Shop.text)

        label1.grid(row = 1, column = 0 )
        label2.grid(row = 1, column = 1)
        label3.grid(row = 2, column = 0)
        button1 = Button(self, text = "Pause",\
                         command = lambda: controller.show_frame("Pause"))
        button2 = Button(self, text = "Game",\
                         command = lambda: controller.show_frame("Game"))
        buttonSw = Button(self, text = "Buy Sword for 10",\
                          command = self.buy("sword"))
        button1.grid(row = 0, column = 0 )
        button2.grid(row = 0, column = 1 )
        buttonSw.grid(row = 3, column = 0)
        
        
    def buy(self, value):
        response = "You should never see this"
        if value == "sword":
            response = "You don't have enough"
            if Shop.player.coins >= 10:
                response = "You buys a better sword"
                Shop.player.coins -= 10
                Shop.player.atk += 1

                
        self.setStatus(response)

    def setStatus(self, status):
        Shop.text = status
            
                          
        


#############
# RUNTIME
#############
# the default size of the GUI is 800x600
WIDTH = 800
HEIGHT = 600

window = Manager()
window.mainloop()
    
