```
 ____   _                _           _   _                   ____
/ ___| (_) _ __    __ _ | |  ___    | | | |___  ___  _ __   |  _ \  _   _  _ __    __ _   ___  ___   _ __
\___ \ | || '_ \  / _` || | / _ \   | | | / __|/ _ \| '__|  | | | || | | || '_ \  / _` | / _ \/ _ \ | '_ \
 ___) || || | | || (_| || ||  __/   | |_| \__ \  __/| |     | |_| || |_| || | | || (_| ||  __/ (_) || | | |
|____/ |_||_| |_| \__, ||_| \___|    \___/|___/\___||_|     |____/  \__,_||_| |_| \__, | \___|\___/ |_| |_|
                  |___/                                                           |___/
```

# SUD Engine

SUD means for "Single User Dungeon": it's like a Multi User Dungeon (MUD) but for single player. In other words, it's a text-mode adventure with elements of both Role Playing Games and sandbox PC games. This is supposed to be just a game engine, not a playable game.

This game engine is being developed as from the scripts created by Tomas Varaneckas (Vilnius, Lithuania), and released on [his website](Http://paranoid-engineering.blogspot.com/2008/11/python-mud-game-example.html) on November 28th, 2008.

REQUIREMENTS:

* Python 3+

RUNNING:

1. Windows: double click start.py

2. Linux, in terminal: python3 start.py

3. Type "help" while in game for commands

KNOWN BUGS:

* When an object is placed in the inventory and there is already an object with the same name inside it, then that object disappears, leaving only one.
