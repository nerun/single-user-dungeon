#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from libraries import *

# Language interface file
engine = language["engine"]

# CLASS OBJECTS ================================================================
class SudObject:
    def __init__(self, name, sight, collide = engine["nothing_happens"], usability = engine["unusable"]):
        self.name = name
        self.sight = sight.capitalize()
        self.collide = collide.capitalize()
        self.usability = usability.capitalize()
    def view(self):
        return self.sight + "\n"
    def touch(self):
        return self.collide + "\n"
    def use(self):
        return self.usability + "\n"

# CLASS PLAYER =================================================================
class SudPlayer:
    def __init__(self, name):
        self.inventory = {}
        self.name = name
        self.ST = 10
        self.DX = 10
        self.IQ = 10
        self.HT = 10
    def drop(self, name):
        if name in self.inventory:
            return self.inventory.pop(name)
    def move(self, area):
        ClearScreen()
        return area.view()
    def say(self, what):
        return engine["you_says"] % (what) + '\n'
    def status(self, args):
        status = engine["char_sheet"] % (self.name, self.ST, self.DX, self.IQ, self.HT)
        return status
    def take(self, obj):
        self.inventory[obj.name] = obj
        return engine["placed_inventory"] % (obj.name) + "\n"
    def touch(self, name):
        if name in self.inventory:
            return self.inventory[name].touch()
    def use(self, what):
        if what in self.inventory:
            return self.inventory[what].use()
        else:
            return engine["you_not_have"] % (what) + '\n'

# CLASS AREA ===================================================================
class SudArea:
    def __init__(self, sight):
        self.objects = {}
        self.panorama = {}
        self.sight = sight
        self.inverted_directions = {'north':'south', 'south':'north', 'east':'west', 'west':'east'}

    def addArea(self, direction, area):
        area.panorama[self.inverted_directions[direction]] = self
        self.panorama[direction] = area

    def relocate(self, args):
        try:
            return self.panorama[args]
        except KeyError:
            return None

    def addObject(self, obj):
        if obj != None:
            self.objects[obj.name] = obj
            return engine["item_was_dropped"] % (obj.name) + "\n"

    def getObject(self, name):
        if name in self.objects:
            return self.objects.pop(name)
        else:
            return engine["there_isnt_around"] % (name) + "\n"

    def touchObject(self, name):
        if name in self.objects:
            return self.objects[name].touch()
        else:
            return engine["there_isnt_around"] % (name) + "\n"

    def view(self, args = 'around'):
        if (args != '' and args != 'around'):
            try:
                return self.panorama[args].view()
            except KeyError:
                try:
                    return self.objects[args].view()
                except KeyError:
                    return engine["there_isnt_around"] % (args) + "\n"
        else:
            objects = []
            for v in self.objects.items():
                objects.append(v[0])
            objects = sorted(objects)
            for i in objects:
                if i[0] in ('a','e','i','o','u'):
                    objects[objects.index(i)] = engine["an_item_is_here"] % (i)
                else:
                    objects[objects.index(i)] = engine["a_item_is_here"] % (i)
            objectsStr = '\n'.join(objects)
            if (len(objects) >= 1):
                obsight = prcolor(3,'\n' + objectsStr)
            else:
                obsight = ''
            return self.sight + obsight

# CLASS COMMANDS ===============================================================
class SudCommand:
    __doc__ = "\n " + engine["available_commands"] + "\n"
    
    def __init__(self, char, area):
        self.char = char
        self.area = area

    def drop(self, args):
        return self.area.addObject(self.char.drop(args))
    drop.__doc__ = "\n " + engine["drop"] + "\n"

    def d(self, args):
        return self.drop(args)
    d.__doc__ = "\n " + engine["d"] + "\n"

    def exit(self, args):
        print(prcolor(5, "\n " + engine["bye"]  + "\n"))
        exit()
    exit.__doc__ = "\n " + engine["exit"] + "\n"

    def x(self, args):
        return self.exit(args)
    x.__doc__ = "\n " + engine["x"] + "\n"

    def quit(self, args):
        return self.exit(args)
    quit.__doc__ = "\n " + engine["quit"] + "\n"

    def q(self, args):
        return self.exit(args)
    q.__doc__ = "\n " + engine["q"] + "\n"

    def get(self, args):
        try:
            return self.char.take(self.area.getObject(args))
        except AttributeError:
            return engine["cant_take"] + ' ' + args + '.\n'
    get.__doc__ = "\n " + engine["get"] + "\n"

    def g(self, args):
        return self.get(args)
    g.__doc__ = "\n " + engine["g"] + "\n"

    def help(self, args):
        if args == '':
            return self.__doc__
        else:
            try:
                return getattr(self, args).__doc__
            except AttributeError:
                return prcolor(1,engine["help_topic_not_found"]) + "\n\n " + engine["available_commands"] + "\n"
    help.__doc__ = "\n " + engine["help"] + "\n"

    def h(self, args):
        return self.help(args)
    h.__doc__ = "\n " + engine["h"] + "\n"

    def inventory(self, args):
        if len(self.char.inventory) > 0:
            return engine["your_inventory"] + ':\n - ' + '\n - '.join(self.char.inventory) + '\n'
        else:
            return engine["inventory_empty"] + "\n"
    inventory.__doc__ = "\n " + engine["inventory"] + "\n"

    def i(self, args):
        return self.inventory(args)
    i.__doc__ = "\n " + engine["i"] + "\n"

    def look(self, args):
        if args == "":
            ClearScreen()
        return self.area.view(args)
    look.__doc__ = "\n " + engine["look"] + "\n"

    def l(self, args):
        return self.look(args)
    l.__doc__ = "\n " + engine["l"] + "\n"

    def move(self, args):
        area = self.area.relocate(args)
        if area != None:
            self.area = area
            return self.char.move(self.area)
        else:
            return engine["nothing_that_way"] + "\n"
    move.__doc__ = "\n " + engine["move"] + "\n"

    def n(self, args):
        return self.move('north')
    n.__doc__ = "\n " + engine["n"] + "\n"

    def s(self, args):
        return self.move('south')
    s.__doc__ = "\n " + engine["s"] + "\n"

    def e(self, args):
        return self.move('east')
    e.__doc__ = "\n " + engine["e"] + "\n"

    def w(self, args):
        return self.move('west')
    w.__doc__ = "\n " + engine["w"] + "\n"

    def say(self, args):
        return self.char.say(args)
    say.__doc__ = "\n " + engine["say"] + "\n"

    def y(self, args):
        return self.say(args)
    y.__doc__ = "\n " + engine["y"] + "\n"

    def status(self, args):
        return self.char.status(args)
    status.__doc__ = "\n " + engine["status"] + "\n"

    def st(self, args):
        return self.status(args)
    st.__doc__ = "\n " + engine["st"] + "\n"

    def touch(self, args):
        if args in self.char.inventory:
            return self.char.touch(args)
        else:
            return self.area.touchObject(args)
    touch.__doc__ = "\n " + engine["touch"] + "\n"

    def t(self, args):
        return self.touch(args)
    t.__doc__ = "\n " + engine["t"] + "\n"

    def use(self, args):
        return self.char.use(args)
    use.__doc__ = "\n " + engine["use"] + "\n"

    def u(self, args):
        return self.use(args)
    u.__doc__ = "\n " + engine["u"] + "\n"

# CLASS GAME ===================================================================
class SudGame:
    def __init__(self, char, area):
        self.cmd = SudCommand(char, area)
        self.FirstSight = area.view()

    def run(self):
        print(self.FirstSight)
        while True:
            try:
                command = input('> ');
            except EOFError:
                print("")
                quit()
            self.parse(command)

    def parse(self, command):
        comm = command.lower().split(' ')
        
        try:
            cmd = comm[0]
        except IndexError:
            cmd = 'help'
        
        try:
            args = comm[1:]
        except IndexError:
            args = []
        
        try:
            result = getattr(self.cmd, cmd)(' '.join(args).strip())
        except AttributeError:
            result = prcolor(1,engine["unknown_command"]) + "\n\n " + engine["available_commands"] + "\n"
        
        print(result)
