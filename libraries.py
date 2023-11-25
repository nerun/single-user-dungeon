#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Defines common routines
import os, locale, json

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
