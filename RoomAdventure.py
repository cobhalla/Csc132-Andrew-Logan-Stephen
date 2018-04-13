######################################################################
# Name:  Andrew Hall       
# Date:     16 March 2018
#           1 April 2018
# Description:  A room game with bonus features
######################################################################
# Various import statements for making and using the GUI
from Tkinter import *




######################################################################


# the blueprint for a room
class Room(object):
    # the constructor
    def __init__(self, name, image):
        # rooms have a name, an image (the name of a file),
        # exits (e.g., south), exit locations
        # (e.g., to the south is room n), items (e.g., table), item
        # descriptions (for each item), and grabbables (things that
        # can be taken into inventory)
        self.name = name
        self.image = image
        self.exits = {}
        self.items = {}
        self.grabbables = []

    # Getters and setters for the instance variables
    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, value):
        self._name = value
        
    @property
    def image(self):
        return self._image
    @image.setter
    def image(self, value):
        self._image = value
        
    @property
    def exits(self):
        return self._exits
    @exits.setter
    def exits(self, value):
        self._exits = value
        
    @property
    def items(self):
        return self._items
    @items.setter
    def items(self, value):
        self._items = value
        
    @property
    def grabbables(self):
        return self._grabbables
    @grabbables.setter
    def grabbables(self, value):
        self._grabbables = value
        
    # adds an exit to the room
    # the exit is a string (e.g., north)
    # the room is an instance of a room
    def addExit(self, exite, room):
        # append the exit and room to the appropriate lists
        self._exits[exite] = room
        
    # adds an item to the room
    # the item is a string (e.g., table)
    # the desc is a string that describes the item (e.g., it is made
    # of wood)
    def addItem(self, item, desc):
        # append the item and description to the appropriate lists
        self._items[item] = desc

    # adds a grabbable item to the room
    # the item is a string (e.g., key)
    def addGrabbable(self, item):
        self._grabbables.append(item)

    # removes a grabbable item from the room
    # the item is a string (e.g., key)
    def delGrabbable(self, item):
        # remove the item from the list
        self._grabbables.remove(item)

    def __str__(self):
        # first, the room name
        s = "You are in {}.\n".format(self.name)
        
        # next, the items in the room
        s += "You see: "
        for item in self.items:
            s += item + " "
        s += "\n"

        # next, the exits from the room
        s += "Exits: "
        for exit in self.exits:
            s += exit + " "

        return s

# the game class
# this inherits from the Frame class of TKinter
class Game(Frame):
    #the constructor
    def __init__(self, parent):
        #call the constructor in the superclass
        Frame.__init__(self, parent)

    # creates the rooms
    def createRooms(self):
        # r1 through r4 are the four rooms in the mansion
        # currentRoom is the room the player is currently in (which can
        # be one of r1 through r4)
        # since it needs to be changed in the main part of the program,
        # it must be global
        #global currentRoom
        # create the rooms and give them meaningful names and an
        # image in the current directory
        r1 = Room("Room 1", "room1.gif")
        r2 = Room("Room 2", "room2.gif")
        r3 = Room("Room 3", "room3.gif")
        r4 = Room("Room 4", "room4.gif")
        n1 = Room("Narnia", "Narnia.gif")
        n2 = Room("Road 1", "Road1.gif")
        n3 = Room("Road 2", "Road1.gif")
        n4 = Room("Cave", "cave.gif")
        g1 = Room("PayGate", "gate.gif")
        # add exits to room 1
        r1.addExit("east", r2) # -> to the east of room 1 is room 2
        r1.addExit("south", r3)
        # add grabbables to room 1
        r1.addGrabbable("key")
        # add items to room 1
        r1.addItem("chair", "It is made of wicker and no one is sitting on it.")
        r1.addItem("table", "It is made of oak. A golden key rests on it.")
        # add exits to room 2
        r2.addExit("west", r1)
        r2.addExit("south", r4)
        # add items to room 2
        r2.addItem("rug", "It is nice and Indian. It also needs to be vacuumed.")
        r2.addItem("fireplace", "It is full of ashes.")
        # add exits to room 3
        r3.addExit("north", r1)
        r3.addExit("east", r4)
        # add grabbables to room 3
        r3.addGrabbable("book")
        # add items to room 3
        r3.addItem("bookshelves", "They are empty. Go figure.")
        r3.addItem("statue", "There is nothing special about it.")
        r3.addItem("desk", "The statue is resting on it. So is a book.")
        # add exits to room 4
        r4.addExit("north", r2)
        r4.addExit("west", r3)
        r4.addExit("south", None) # DEATH!
        # add grabbables to room 4
        r4.addGrabbable("6-pack")
        # add items to room 4
        r4.addItem("brew_rig", "Gourd is brewing some sort of oatmeal stout on the brew rig. A 6-pack is resting beside it.")
        # set room 1 as the current room at the beginning
        # of the game
        #add exits to Narnia
        n1.addExit("portal", r2)
        n1.addExit("east" , n2)
        n1.addExit("west" , n3)
        n1.addExit("north", g1) 
        # add grabables to Narnia
        #n1.addGrabbable("thing")do this one later
        #add items to Narnia
        n1.addItem("???", "A strange man stands beside a gas lamp that flickers\n He is holding something")
        n1.addItem("sign", "North : 'North expansion $5.99' \nEast : Castle \nWest : Cave Of Horror")
        #add exits to Road1
        n2.addExit("west", n1)
        n2.addItem("shrub", "A very small shrub is planted in the middle of the road.\nYou cant get past.")
        n2.addGrabbable("leaf")
        #add exits to Road2
        n3.addExit("east", n1)
        n3.addExit("west", n4)

        #add payGate
        g1.addExit("south", n1)
        g1.addItem("gate", "You shall not pass!!!\nYour questions fall on the ground.")
        g1.addGrabbable("why")
        g1.addGrabbable("who")
        g1.addGrabbable("what")
        g1.addGrabbable("when")
        g1.addGrabbable("where")
        

        #add exits tot cave
        n4.addExit("east", n3)
        n4.addGrabbable("lamp")
        n4.addItem("cave", "A very deep cave.\nThere is a lamp near the enterance.")
        
        Game.currentRoom = r1
        # initialize the player's inventory
        Game.inventory = []
        #so you can set up things to send you wherever you want
        Game.roomLib = {"Room1" : r1, "Room2" : r2, "Room3" : r3, "Room4" : r4, "Narnia" : n1,\
                        "Road 1" : n2, "Road 2" : n3, "Cave" : n4, "Gate" : g1}
        
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

        
    # set the current room image
    def setRoomImage(self):
        if(Game.currentRoom == None):
            # if dead, set the skull image
            Game.img = PhotoImage(file = "skull.gif")
        else:
            # otherwise grab the image for the current room
            Game.img = PhotoImage(file = Game.currentRoom.image)

        # display the image on the left of the GUI
        Game.image.config(image = Game.img)
        Game.image.image = Game.img
        
            
    #sets the status displayed on the Right of the GUI
    def setStatus(self, status):
        # enable the text widget, clear it, set it, and disabled it
        Game.text.config(state = NORMAL)
        Game.text.delete("1.0", END)
        if (Game.currentRoom == NONE):
            # if dead, let the player know
            Game.text.insert(END, "YOU DIED! You should just QUIT.\n")
        else:
            # otherwise
            Game.text.insert(END, str(Game.currentRoom) +\
                             "\nYou are carrying: " + str(Game.inventory) +\
                             "\n\n" + status)
            Game.text.config(state = DISABLED)
            

    def play(self):
        #add the rooms to the game
        self.createRooms()
        #configure the GUI
        self.setupGUI()
        #set the current room
        self.setRoomImage()
        #set the current status
        self.setStatus("")
    
    #process the player's input
    def process(self, event):
        # grab the player's input from the input at the bottom of
        # the GUI
        action = Game.player_input.get()
        # set the user's input to lowercase to make it easier to compare
        # the verb and noun to known values
        action = action.lower()
        # set a default response
        response = "I don't understand. Try verb noun.\
                    Valid verbs are go, look, use, and take"
        # exit the game if the player wants to leave (supports quit,
        if (action == "quit" or action == "exit" or action == "bye"\
            or action == "sionara!"):
            exit(0)

        # if the player is dead if goes/went south from room 4
        if(Game.currentRoom == None):
            # clear the player's input
            Game.player_input.delete(0, END)
            return
        
        # split the user input into words (words are separated
        # by spaces) and store the words as a list
        words = action.split()
        
         # two word inputs
        if (len(words) == 2):
            # isolate the verb and noun
            verb = words[0]
            noun = words[1]
            
            # the verb is: go
            if (verb == "go"):
                # set a default response
                response = "Invalid exit."
                # check for valid exits in the current room
                if (noun in Game.currentRoom.exits):
                    # if one id found, change the current room to
                    # the one that is associated with the
                    # specified exit
                    Game.currentRoom =Game.currentRoom.exits[noun]
                    # set the response (success)
                    response = "Room Changed"
                    
            # the verb is: look
            elif (verb == "look"):
                # set a default response
                response = "I don't see that item."

                # check for valid items in the current room
                if (noun in Game.currentRoom.items):
                    # if one is found, set the response to the
                    # item's description
                    response = Game.currentRoom.items[noun]
            # the verb is: take
            elif (verb == "take"):
                # set a default response
                response = "I don't see that item."
                
                # check for valid grabbable items in the
                # current room
                for grabbable in Game.currentRoom.grabbables:
                    # a valid grabbable item is found
                    if (noun == grabbable):
                        # add the grabbable item to the player's
                        # inventory
                        Game.inventory.append(grabbable)
                        # remove the grabbable item from the room
                        Game.currentRoom.delGrabbable(grabbable)
                        # set the response (success)
                        response = "Item grabbed."
                        # no need to check any more
                        # grabbable items
                        break
                    
        # three word inputs
        if(len(words) == 3):
            # isolates words
            verb = words[0]
            noun1 = words[1]
            noun2 = words[2]

            if(verb == "use"):

                # default response
                resopnse = "cannot use that here"
                #genaric
##                if (noun1 == "grabbable"):
##                    if(noun2 == "item"):
##                        #some actions here
##                        break
                if(noun1 == "book" and ("book" in Game.inventory)):
                    if(noun2 == "fireplace"):
                        if(Game.currentRoom.name == "Room 2"):
                            response = "NO, don't do that!"
                        else:
                            response = "You aren't in the right room"
                            
                    if(noun2 == "papers" and ("papers" in Game.inventory)):
                        response = "You use the papers to decode the book and you find a code"
                        Game.inventory.append("code")
                
                if(noun1 == "key" and ("key" in Game.inventory)):
                    if(noun2 == "desk"):
                        if(Game.currentRoom.name == "Room 3"):
                            response = "You open a drawer and find some papers."
                            Game.inventory.append("papers")
                        else:
                            response = "You aren't in the right room"
                
                if(noun1 == "code" and ("code" in Game.inventory)):
                    if(noun2 == "rug"):
                        if(Game.currentRoom.name == "Room 2"):
                            response = "You see the meaning of life emerge from the swirling patterns"
                            Game.inventory.append("42")
                        else:
                            response = "You aren't in the right room"
                            
                if(noun1 == "42" and ("42" in Game.inventory)):
                    if(noun2 == "fireplace"):
                        if(Game.currentRoom.name == "Room 2"):
                            response = "A portal appears and you step through it"
                            Game.currentRoom = Game.roomLib["Narnia"]
                        else:
                            response = "You aren't in the right room"

                if(noun1 == "6-pack" and ("6-pack" in Game.inventory)):
                    if(noun2 == "self"):
                        response = "MMMMMM Beer"
                        Game.inventory.remove("6-pack")
                        Game.inventory.append("5-pack")
                    if(noun2 == "???"):
                        if("thing" in Game.inventory):
                            response = "I'm given err all shes got Cap'm!"
                        else:
                            response = "The other guy didn'd buy me a drink first, have this..."
                            Game.inventory.remove("6-pack")
                            Game.inventory.append("5-pack")
                            Game.inventory.append("thing")
                if(noun1 == "5-pack" and ("5-pack" in Game.inventory)):
                    if(noun2 == "self"):
                        response = "MMMMMM Beer"
                        Game.inventory.remove("5-pack")
                        Game.inventory.append("4-pack")
                    if(noun2 == "???"):
                        if("thing" in Game.inventory):
                            response = "I'm given err all shes got Cap'm!"
                        else:
                            response = "The other guy didn'd buy me a drink first, have this..."
                            Game.inventory.remove("5-pack")
                            Game.inventory.append("4-pack")
                            Game.inventory.append("thing")
                if(noun1 == "4-pack" and ("4-pack" in Game.inventory)):
                    if(noun2 == "self"):
                        response = "MMMMMM Beer"
                        Game.inventory.remove("4-pack")
                        Game.inventory.append("3-pack")
                    if(noun2 == "???"):
                        if("thing" in Game.inventory):
                            response = "I'm given err all shes got Cap'm!"
                            Game.inventory.remove("4-pack")
                            Game.inventory.append("3-pack")
                        else:
                            response = "The other guy didn'd buy me a drink first, have this..."
                            Game.inventory.append("thing")
                if(noun1 == "3-pack" and ("3-pack" in Game.inventory)):
                    if(noun2 == "self"):
                        response = "MMMMMM Beer"
                        Game.inventory.remove("3-pack")
                        Game.inventory.append("2-pack")
                    if(noun2 == "???"):
                        if("thing" in Game.inventory):
                            response = "I'm given err all shes got Cap'm!"
                        else:
                            response = "The other guy didn'd buy me a drink first, have this..."
                            Game.inventory.remove("3-pack")
                            Game.inventory.append("2-pack")
                            Game.inventory.append("thing")
                if(noun1 == "2-pack" and ("2-pack" in Game.inventory)):
                    if(noun2 == "self"):
                        response = "MMMMMM Beer"
                        Game.inventory.remove("2-pack")
                        Game.inventory.append("1-pack")
                    if(noun2 == "???"):
                        if("thing" in Game.inventory):
                            response = "I'm given err all shes got Cap'm!"
                        else:
                            response = "The other guy didn'd buy me a drink first, have this..."
                            Game.inventory.remove("2-pack")
                            Game.inventory.append("1-pack")
                            Game.inventory.append("thing")
                if(noun1 == "1-pack" and ("1-pack" in Game.inventory)):
                    if(noun2 == "self"):
                        response = "MMMMMM Beer"
                        Game.inventory.remove("6-pack")
                    if(noun2 == "???"):
                        response = "I will not take your last one!"

                if(noun1 == "thing" and ("thing" in Game.inventory)):
                    if(noun2 == "statue"):
                        if(Game.currentRoom.name == "Room 3"):
                            response = "Bold and Brash? More like BELONGS IN THE TRASH!!!"
                    if(noun2 == "e"):
                        response = "you make a 'thinge'"
                        Game.inventory.remove("e")
                        Game.inventory.append("thinge")

                if(noun1 == "lamp" and ("lamp" in Game.inventory)):
                    if(noun2 == "cave"):
                        if(Game.currentRoom.name == "Cave"):
                            response = "You find... SomEthing..."
                            Game.inventory.append("e")
                            
                if(noun1 == "thinge" and ("thinge" in Game.inventory)):
                    if(noun2 == "why" and ("why" in Game.inventory)):
                        response = "WhaT aRE ThoSe???"
                        Game.inventory.remove("thinge")
                        Game.inventory.remove("why")
                        Game.inventory.append("thingey")
                        
                if(noun1 == "thingey" and ("thingey" in Game.inventory)):
                    if(noun2 == "self"):
                        response = "You Won!"

                if(noun1 == "what"  and ("what" in Game.inventory)):
                    if(noun2 == "self"):
                        response = "I do not want to know"
                    if(noun2 == "table"):
                        response = "A Table"
                    if(noun2 == "chair"):
                        response = "A Chair"
                    if(noun2 == "desk"):
                        response = "I do not want to know"
                    if(noun2 == "rug"):
                        response = "A Rug"
                    if(noun2 == "fireplace"):
                        response = "A Portal to HELL"
                    if(noun2 == "brew_rig"):
                        response = "Something to make Laudnum with"
                    if(noun2 == "42"):
                        response = "The meaning to life, the universe, and everything"
                    if(noun2 == "book"):
                        response = "A leather bound Tome of Arkane Knowlege"
                    if(noun2 == "key"):
                        response = "A Key"
                    if(noun2 == "leaf"):
                        response = "Why do you even have these?"
                    if(noun2 == "4th_wall"):
                        response = "Nope"
                if(noun1 == "who"  and ("who" in Game.inventory)):
                    if(noun2 == "self"):
                        response = "I do not want to know"
                    
                    
                    
                    
                        
                            
                
                    
                        
            
                    
                            

                        

                

            
        # display the response on the right of the GUI
        # display the room's image on the left of the GUI
        # clear the player's input
        self.setStatus(response)
        self.setRoomImage()
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
