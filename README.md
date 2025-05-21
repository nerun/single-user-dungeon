```
   ____     _   _     ____
  / ___|   | | | |   |  _ \
  \___ \   | | | |   | | | |
   ___) |_ | |_| | _ | |_| |_
  |____/(_) \___/ (_)|____/(_)
```

[![Python](https://img.shields.io/badge/Python_3-%23244d70?style=flat&logo=python&logoColor=%23ffde58)](https://www.python.org/) [![MIT License](https://img.shields.io/badge/License-%25?style=flat&label=MIT&color=olive)](https://en.wikipedia.org/wiki/MIT_License)


# Single User Dungeon

Text-based adventure engine  
Inspired by classic [MUDs](https://en.wikipedia.org/wiki/Multi-user_dungeon), focused on **single-player** experience.

Written in [Python](https://www.python.org)  
Create & explore interactive dungeons with RPG & sandbox elements.

Data & translations via JSON files — easy customization.

> [!Note]
> This game engine is being developed as from the scripts created by Tomas Varaneckas (Vilnius, Lithuania), and released on his blog [Paranoid Engineering](Http://paranoid-engineering.blogspot.com/2008/11/python-mud-game-example.html) on November 25th, 2008.

---

## Requirements

- Python 3.8+
- Standard libs: `json`, `os`, `locale`, `pathlib`
- No external dependencies

---

## Installation & Running

```bash
$ git clone https://github.com/nerun/single-user-dungeon.git
$ cd single-user-dungeon/src
$ python3 -m game.main
```

**Tip:** type `help` inside the game for commands.

---

## Localization

- Game content (rooms, objects, UI) in `language/` folder JSON files.
- Add new language: create `<locale_code>.json` (e.g., `fr_FR.json`).
- Edit manually or with Poedit (v3.3+).
- Auto-detects system locale, defaults to English if missing.

---

## License

MIT License — see [LICENSE](https://github.com/nerun/single-user-dungeon/raw/main/LICENSE)
