#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import textwrap
from engine import *

# OBJECTS
# object_name : class engine.SudObject <name, look, touch, use>
ObjectsDic = {}

for i in language["objects"]:
    ObjectsDic[i] = SudObject(i, language["objects"][i]["look"],
                              language["objects"][i]["touch"],
                              language["objects"][i]["use"])

# ROOMS
# room_number : class engine.SudArea (Exits, Room title, Room description)
RoomsDic = {}

# Show rooms' description to player in friendly format
# Creates engine.SudArea.sight
def ShowRoom(roomsdic, roomNum):
    def printw(text, columns=80, indent=4):
        paragraphs = text.splitlines()
        textOut = "\n".join([textwrap.fill(p, columns, replace_whitespace=False,
                                           initial_indent=' '*indent) for p in paragraphs])
        return textOut
    
    Title = prcolor(6, roomsdic[roomNum]["title"])
    
    exits = ""
    
    for i in roomsdic[roomNum]["exits"]:
        exits += i[0] + " "
    
    Exits= "[ Exits: " + prcolor(3, exits) + "]"
    
    Desc = printw(roomsdic[roomNum]["description"])
    
    return Title + "\n" + Exits + "\n" + Desc + "\n"

for i in language["rooms"]:
    # "i" is the room number as string
    desc = ShowRoom(language["rooms"], i)
    # 'ID' : Class(string: Room title, Exits, Room description)
    RoomsDic[i] = SudArea(desc)

# SPAWN OBJECTS AUTOMATICALLY
# "room" is the room number as string
# "spawn" is the object to be spawned as string
for room in language["rooms"]:
    for spawn in language["rooms"][room]["spawns"]:
        RoomsDic[room].addObject(ObjectsDic[spawn])

# LINK ALL AREAS WITH BIDIRECTIONAL REFERENCES AUTOMATICALLY
for room in RoomsDic:
    exits = language["rooms"][room]["exits"]
    for directions in exits:
        RoomsDic[room].addArea(directions, RoomsDic[exits[directions]])

# CREATES A CHARACTER
char = SudPlayer('Test Player Name')

# CREATE A GAME WITH PLAYER AND STARTING AREA
game = SudGame(char, RoomsDic['1'])

# START IT!
ClearScreen()
game.run()
