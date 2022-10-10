# This file define what exists in the world.
import glob, copy, json
from libraries import *
from engine import *

# CREATE A DICTIONARY READING FILES IN A FOLDER
# FilesToDict(*Path, ValidExt, If is room then put yes if not let blank)
def FilesToDict(Path, Ext, IsRoom='no'):
    ListOfFiles = glob.glob(os.path.join(Path, '*' + Ext))
    ListOfFilesB = copy.copy(ListOfFiles)

    rList = (Path, Ext, "/", "\\")

    if IsRoom.lower() == "yes":
        for n, i in enumerate(ListOfFilesB):
            for j in rList:
                i = i.replace(j,'')
            ListOfFilesB[n] = i

        for n, i in enumerate(ListOfFilesB):
            try:
                int(i)
            except ValueError:
                ListOfFiles.pop(n)

    Dict = {}

    for i in ListOfFiles:
        fileread = open(i,"r")
        thisfile = fileread.readlines()
        fileread.close()
        for i in thisfile:
            thisfile[0] = thisfile[0].replace('\n','')
            if IsRoom.lower() == "yes":
                thisfile[1] = thisfile[1].replace('\n','')
                thisfile[2] = thisfile[2].replace('\n','')
        thisfilelist = list(thisfile)
        if IsRoom.lower() == "yes":
            thisfilelist[1] = json.loads(thisfilelist[1])
        Dict[thisfilelist[0]] = thisfilelist[1:]

    return Dict

# SHOW ROOM DESCRIPTION TO PLAYER IN FRIENDLY FORMAT
# Creates SudArea.sight (engine.py)
# ShowRoom(FilesToDict(RoomsPath, ValidExt, 'yes'),'1')
# Rooms = rooms dictionary
# Number = specific room number (ID)
def ShowRoom(Rooms, Number):
    return prcolor(6, Rooms[Number][2]) + '[ Exits: ' + prcolor(7, ' '.join(list(Rooms[Number][0]))) + ' ]\n' + ' '.join(Rooms[Number][3:])

# Defines default paths and valid extension for files
RoomsPath = 'rooms'
ObjectsPath = 'objects'
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

# ROOMS
# Read folder "rooms" and create dictionary reading files in there
# IDs : (Exits, Room title, Room description)
BaseRoomsDic = FilesToDict(RoomsPath, ValidExt, 'yes')
# Void final dictionary of rooms
RoomsDic = {}
# Fulfill final dictionary of rooms
for i in BaseRoomsDic:
    # "i" is the room number
    desc = ShowRoom(BaseRoomsDic, i)
# 'ID' : Class(string: Room title, Exits, Room description)
# To call an area, use 'ID'
    RoomsDic[i] = SudArea(desc)

# Spawn objects automatically by reading rooms files
for i in RoomsDic:
    objects_list = json.loads(BaseRoomsDic[i][1])
    for k in objects_list:
        RoomsDic[i].addObject(ObjectsDic[k])

# Link all areas with bidirectional references automatically
for key in RoomsDic:
    directions = BaseRoomsDic[key][0]
    for j in directions:
        if j == "n":
            j2 = "north"
        elif j == "s":
            j2 = "south"
        elif j == "e":
            j2 = "east"
        elif j == "w":
            j2 = "west"
        RoomsDic[key].addArea(j2, RoomsDic[directions[j]])

# Create a character
char = SudPlayer('Temporary Name')

# Create a game with player and starting area
game = SudGame(char, RoomsDic['1'])

# Lets go!
ClearScreen()
game.run()
