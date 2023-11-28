```
 ____     _   _     ____    
/ ___|   | | | |   |  _ \   
\___ \   | | | |   | | | |  
 ___) |_ | |_| | _ | |_| |_ 
|____/(_) \___/ (_)|____/(_)
```

# Single User Dungeon

**Single User Dungeon** is a text-based adventure with elements of tabletop RPG and sandbox games for PC. It is inspired by the old [Multi-User Dungeons (MUDs)](https://en.wikipedia.org/wiki/Multi-user_dungeon) but focused on individual play. It is assumed that this is just a game engine, not a playable game, and that it is more for fun and studying [Python](https://www.python.org/) than serious development.

This game engine is being developed as from the scripts created by Tomas Varaneckas (Vilnius, Lithuania), and released on his blog [Paranoid Engineering](Http://paranoid-engineering.blogspot.com/2008/11/python-mud-game-example.html) on November 25th, 2008.

### Easy to translate

SUD is easy to translate because it uses JSON files to store information about rooms, objects, and the game interface. You can use the [Poedit](https://poedit.net/) program, which in version 3.3+ added support for JSON files, and version 3.4 is now available as a flatpak in the Ubuntu/Mint stores.

### Requirements

* Python 3+

### Running

1. Start:
   - **Windows**: double click start.py
   - **Linux**: in terminal `python3 start.py`
2. Type "help" while in game for commands

### Known bugs

* When an object is placed in the inventory and there is already an object with the same name inside it, then that object disappears, leaving only one.
