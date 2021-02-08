# Defines common routines
import os, glob, copy

# COLORED TEXT
# Example:
# prcolor(1, "prints a red text here")
def prcolor(color, text):
    # color:
    # 1 Red
    # 2 Green
    # 3 Yellow / Orange
    # 4 Blue
    # 5 Purple
    # 6 Cyan (Light Blue)
    # 7 Light Gray
    # 8 Black
    return '\033[9' + str(color) + 'm' + text + '\033[00m'

# CLEAR SCREEN
def ClearScreen(lines=100):
    if os.name == 'posix':
        os.system('clear')
    elif os.name in ('nt', 'dos', 'ce'):
        os.system('cls')
    else:
        print('\n' * lines)

# CREATE A DICTIONARY READING FILES IN A FOLDER
# FilesToDict(*Path, ValidExt, If is room then put yes if not let blank)
def FilesToDict(Path, Ext, IsRoom='no'):
    ListOfFiles = glob.glob(Path + '*' + Ext)
    ListOfFilesB = copy.copy(ListOfFiles)

    if IsRoom.lower() == "yes":
        for n, i in enumerate(ListOfFilesB):
            a = i.replace(Path,'')
            b = a.replace(Ext,'')
            ListOfFilesB[n] = b

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
        thisfiletuple = tuple(thisfile)
        Dict[thisfiletuple[0]] = thisfiletuple[1:]

    return Dict

# SHOW ROOM DESCRIPTION TO PLAYER IN FRIENDLY FORMAT
# ShowRoom(FilesToDict(RoomsPath, ValidExt, 'yes'),'1')
# Rooms = rooms dictionary
# Number = specific room number (ID)
def ShowRoom(Rooms, Number):
    return prcolor(6, Rooms[Number][1]) + '\n[ Exits: ' + prcolor(7,' '.join(list(Rooms[Number][0]))) + ' ]\n' + ' '.join(Rooms[Number][2:])
