#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Defines common routines
import os, locale, json

# FORMATTED TEXT
# span('text red in italic', 'red', 'i')
def span(txt='missing text', color='', style=''):
    txt = str(txt)
    color = str(color).lower()
    style = str(style).lower()

    colors = {
        '': '', 'black':'30', 'red':'31', 'green':'32', 'yellow':'33', 'blue':'34',
        'magenta':'35', 'cyan':'36', 'white':'37',
        'r':'31', 'g':'32', 'y':'33', 'b':'34', 'm':'35', 'c':'36', 'w':'37'
    }

    styles = {
        '': '', 'bold':'1', 'faint':'2', 'italic':'3', 'bold-italic':'1;3',
        'underline':'4', 'blink':'5', 'reverse':'7',
        'b':'1', 'f':'2', 'i':'3', 'bi':'1;3', 'u':'4', 'k':'5', 'm':'7'
    }

    if color not in colors or style not in styles:
        print("""Use: span(string, 'color code', 'style code')

Colors: red (r), green (g), yellow (y), blue (b), magenta (m), cyan (c), white (w)
Styles: bold (b), italic (i), bold-italic (bi), underline (u), faint (f), blink (k),
        reverse (m)
""")
        return '\033[0;7m span(): bad formatted \033[0m'

    codes = []
    if styles[style]:
        codes.append(styles[style])
    if colors[color]:
        codes.append(colors[color])

    if codes:
        return f"\033[{';'.join(codes)}m{txt}\033[0m"
    else:
        return txt

# CLEAR SCREEN
def clear():
    if os.name in ('posix', 'nt', 'dos', 'ce'):
        os.system('clear' if os.name == 'posix' else 'cls')
    else:
        print('\n' * 100)

# PATHSLASH
if os.name in ('nt', 'dos', 'ce'): # Windows
    pathslash = "\\"
else: # Posix
    pathslash = "/"

# DEFINES SYSTEM LANGUAGE FILE =================================================
LangPath = "language" + pathslash

SysLangFilePath = LangPath + locale.getdefaultlocale()[0] + '.json'

try:
    with open(SysLangFilePath) as language_file:
        language = json.load(language_file)
except:
    with open(LangPath + 'en.json') as language_file:
        language = json.load(language_file)
