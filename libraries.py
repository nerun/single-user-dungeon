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

    colors = {'red':'1', 'green':'2', 'yellow':'3', 'blue':'4', 'magenta':'5', 'cyan':'6', 'white':'7', '':'\033[0',
              'r':'1', 'g':'2', 'y':'3', 'b':'4', 'm':'5', 'c':'6', 'w':'7'}
    styles = {'bold':'1', 'faint':'2', 'italic':'3', 'underline':'4', 'blink':'5', 'mark':'7', '':'m',
              'b':'1', 'f':'2', 'i':'3', 'u':'4', 'k':'5', 'm':'7'}

    if color not in colors.keys() or style not in styles.keys():
        print ("""Use: span(string, 'color code', 'style code')

  Colors    red (r), green (g), yellow (y), blue (b), magenta (m), cyan (c),
            white (w)
            
  Styles    bold (b), italic (i), underline (u), faint (f), blink (k),
            mark (m)
""")
        return '\033[0;7m span(): bad formatted \033[0m'
    else:
        color = colors[color]
        style = styles[style]
        
        if color != '\033[0':
            color = '\033[9' + color
            
        if style != 'm':
            style = ';' + style + 'm'

        return color + style + txt + '\033[0m'

# CLEAR SCREEN
def ClearScreen(lines=100):
    if os.name == 'posix':
        os.system('clear')
    elif os.name in ('nt', 'dos', 'ce'):
        os.system('cls')
    else:
        print('\n' * lines)

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
