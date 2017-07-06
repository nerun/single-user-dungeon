# -*- coding: cp860 -*-
# This file define what exists in the world.
import os
from libraries import *
from engine import *

# Defines default paths and valid extension for files
RoomsPath = './rooms/'
ObjectsPath = './objects/'
ValidExt = '.txt'

# Create subdirectories if don't exist
if os.path.isdir(RoomsPath) is False:
 os.mkdir(RoomsPath)
if os.path.isdir(ObjectsPath) is False:
 os.mkdir(ObjectsPath)

# OBJECTS
# Read folder "objects" and create dictionary reading files in there
# name: (look, touch, use)
BaseObjectsDic = FilesToDict(ObjectsPath, ValidExt)
# Void final dictionary of objects
ObjectsDic = {}
# Fulfill final dictionary of objects (object name: atribute 1, attribute 2 etc)
for i in BaseObjectsDic:
# name: Class(name, look, touch, use)
 ObjectsDic[BaseObjectsDic[i]] = MudObject(BaseObjectsDic[i],BaseObjectsDic[i][0],BaseObjectsDic[i][1],BaseObjectsDic[i][2])

# ROOMS
# Read folder "rooms" and create dictionary reading files in there
# IDs : (Exits, Room title, Room description)
BaseRoomsDic = FilesToDict(RoomsPath, ValidExt, 'yes')
# Void final dictionary of rooms
RoomsDic = {}
# Fulfill final dictionary of rooms
for i in BaseRoomsDic:
 desc = ShowRoom(BaseRoomsDic, i)
# ID : Class(string: Room title, Exits, Room description)
 RoomsDic[i] = MudArea(desc)

# ======= TO DO ==============================================================

# Attaching interactive stuff to areas
beach.addObject('crap', poo)
port.addObject('flower', rose)
port.addObject('fruit', apple)
maiden.addObject('bird', sparrow)

# Link all areas with bidirectional references
port.addArea('north', beach)
port.addArea('west', house)
village.addArea('east', maiden)
maiden.addArea('north', port)

# Create a player
char = MudPlayer('Player')

# Create a game with player and starting area
game = MudGame(char, port)

# Lets go!
ClearScreen()
game.run()
