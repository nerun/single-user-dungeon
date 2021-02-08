# -*- coding: cp1252 -*-
# This file define what exists in the world.
import os
from libraries import *
from engine import *

ClearScreen()

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
    ObjectsDic[i] = SudObject(i,BaseObjectsDic[i][0],BaseObjectsDic[i][1],BaseObjectsDic[i][2])

print (ObjectsDic)

# ROOMS
# Read folder "rooms" and create dictionary reading files in there
# IDs : (Exits, Room title, Room description)
BaseRoomsDic = FilesToDict(RoomsPath, ValidExt, 'yes')
# Void final dictionary of rooms
RoomsDic = {}
# Fulfill final dictionary of rooms
for i in BaseRoomsDic:
 desc = ShowRoom(BaseRoomsDic, i)
# 'ID' : Class(string: Room title, Exits, Room description)
# To call an area, use 'ID'
 RoomsDic[i] = SudArea(desc)

# Attaching interactive stuff to areas
RoomsDic['1'].addObject('flower', ObjectsDic['rose']) # porto
RoomsDic['2'].addObject('crap', ObjectsDic['poo']) # praia
RoomsDic['3'].addObject('fruit', ObjectsDic['apple']) # alfandega
RoomsDic['4'].addObject('bird', ObjectsDic['sparrow']) # donzela

# Link all areas with bidirectional references
RoomsDic['1'].addArea('north', RoomsDic['2']) # porto > n > praia
RoomsDic['1'].addArea('west', RoomsDic['3']) # porto > w > alfandega
RoomsDic['4'].addArea('north', RoomsDic['1']) # donzela > n > porto
RoomsDic['5'].addArea('east', RoomsDic['4']) # vila > e > donzela

# Create a player
char = SudPlayer('Player')

# Create a game with player and starting area
game = SudGame(char, RoomsDic['1'])

# Lets go!
ClearScreen()
game.run()
