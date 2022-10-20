#!/usr/bin/env python3
# This file define what exists in the world.
import copy, json, locale, textwrap
import xml.etree.ElementTree as ET
from libraries import *
from engine import *

# Defines system language
SysLang = locale.getdefaultlocale()[0]
DefLang = "en_US"

# Defines default paths and valid extension for files
RoomsPath = 'rooms'
ObjectsPath = 'spawns'
Ext = '.xml'

# Create subdirectories if don't exist
if os.path.isdir(RoomsPath) is False:
    os.mkdir(RoomsPath)
if os.path.isdir(ObjectsPath) is False:
    os.mkdir(ObjectsPath)

# CREATE A DICTIONARY READING FILES IN A FOLDER
# FilesToDict(*Path, If is room then put yes if not let blank)
def FilesToDict(Path, element, IsRoom='no'):
    ListOfFiles = os.listdir(Path)

    Dict = {}
    
    def langchooser(this_room, element_tag):
        if this_room.find(element_tag).find(SysLang) != None:
            return SysLang
        else:
            return DefLang

    for i in ListOfFiles:
        # pathbar is defined in libraries.py as "/" or "\\"
        tree = ET.parse(Path+pathbar+i)
        root = tree.getroot()
        for i in root.findall(element):
            if IsRoom.lower() == "yes":            
                title_lang = langchooser(i, 'title')
                desc_lang = langchooser(i, 'description')
                Dict[i.attrib['id']] = [i.find('exits').attrib, i.find('title').find(title_lang).text, i.find('description').find(desc_lang).text, i.find('spawns')]
            else:
                Dict[i.find('name').text] = [i.find('look').text, i.find('touch').text, i.find('use').text]
    
    return Dict

# SHOW ROOM DESCRIPTION TO PLAYER IN FRIENDLY FORMAT
# Creates SudArea.sight (engine.py)
# ShowRoom(FilesToDict(RoomsPath, 'yes'),'1')
# Rooms = rooms dictionary
# Number = specific room number (ID)
def ShowRoom(roomsdic, roomNum):
    def printw(text, columns=80, indent=4):
        paragraphs = text.splitlines()
        textOut = "\n".join([textwrap.fill(p, columns, replace_whitespace=False,initial_indent=' '*indent) for p in paragraphs])
        return textOut
    
    Title = prcolor(6, roomsdic[roomNum][1])
    
    exits = ""
    
    for i in roomsdic[roomNum][0]:
        exits += i[0] + " "
    
    Exits= "[ Exits: " + prcolor(3, exits) + "]"
    
    Desc = printw(roomsdic[roomNum][2])
    
    return Title + "\n" + Exits + "\n" + Desc + "\n"

# OBJECTS
# Read folder "ObjectsPath" and create dictionary reading files in there
# name: (look, touch, use)
BaseObjectsDic = FilesToDict(ObjectsPath, 'object')

ObjectsDic = {}

for i in BaseObjectsDic:
    # name: Class(name, look, touch, use)
    ObjectsDic[i] = SudObject(i,BaseObjectsDic[i][0],BaseObjectsDic[i][1],BaseObjectsDic[i][2])

# ROOMS
# Read folder "RoomsPath" and create dictionary reading files in there
# IDs : (Exits, Room title, Room description)
BaseRoomsDic = FilesToDict(RoomsPath, 'room', 'yes')

RoomsDic = {}

for i in BaseRoomsDic:
    # "i" is the room number
    desc = ShowRoom(BaseRoomsDic, i)
    # 'ID' : Class(string: Room title, Exits, Room description)
    RoomsDic[i] = SudArea(desc)

# Spawn objects automatically by reading rooms files
# "i" is the room number
for i in BaseRoomsDic:
    for child in BaseRoomsDic[i][3]:
        RoomsDic[i].addObject(ObjectsDic[child.tag])

# Link all areas with bidirectional references automatically
for key in RoomsDic:
    directions = BaseRoomsDic[key][0]
    for j in directions:
        RoomsDic[key].addArea(j, RoomsDic[directions[j]])

# Create a character
char = SudPlayer('Test Player Name')

# Create a game with player and starting area
game = SudGame(char, RoomsDic['1'])

# Lets go!
ClearScreen()
game.run()
