import textwrap
from game.engine import *


def printw(text, columns=80, indent=4):
    paragraphs = text.splitlines()
    textOut = "\n".join([textwrap.fill(p, columns, replace_whitespace=False,
                                       initial_indent=' ' * indent) for p in paragraphs])
    return textOut


def show_room(roomsdic, roomNum):
    title = span(roomsdic[roomNum]["title"], 'cyan', 'bold')
    exits = "".join([i[0] + " " for i in roomsdic[roomNum]["exits"]])
    exits_line = "[ Exits: " + span(exits, 'yellow') + "]"
    desc = printw(roomsdic[roomNum]["description"])
    return title + "\n" + exits_line + "\n" + desc + "\n"


def main():
    # Objects
    objects_dic = {}
    for i in language["objects"]:
        objects_dic[i] = SudObject(
            i,
            language["objects"][i]["look"],
            language["objects"][i]["touch"],
            language["objects"][i]["use"]
        )

    # Rooms
    rooms_dic = {}
    for i in language["rooms"]:
        desc = show_room(language["rooms"], i)
        rooms_dic[i] = SudArea(desc)

    # Spawn objects
    for room in language["rooms"]:
        for spawn in language["rooms"][room]["spawns"]:
            rooms_dic[room].addObject(objects_dic[spawn])

    # Link areas
    for room in rooms_dic:
        exits = language["rooms"][room]["exits"]
        for direction in exits:
            rooms_dic[room].addArea(direction, rooms_dic[exits[direction]])

    # Create player and game
    char = SudPlayer('Test Player Name')
    game = SudGame(char, rooms_dic['1'])

    # Run
    clear()
    game.run()


if __name__ == "__main__":
    main()
