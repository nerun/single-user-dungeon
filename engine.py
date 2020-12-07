import sys
from libraries import *

# CLASS OBJECTS ================================================================
class SudObject:
 def __init__(self, name, sight, collide = 'Nothing happens.', usability = 'Unusable.'):
  self.name = name
  self.sight = sight.capitalize()
  self.collide = collide.capitalize() + '\n'
  self.usability = usability.capitalize() + '\n'
 def view(self):
  return self.sight
 def touch(self):
  return self.collide
 def use(self):
  return self.usability

# CLASS PLAYER =================================================================
class SudPlayer:
 def __init__(self, name):
  self.inventory = {}
  self.name = name
  self.health = 100
 def move(self, area):
  ClearScreen()
  return area.view() + '\n'
 def take(self, obj):
  self.inventory[obj.name] = obj
  return self.name + ' puts ' + obj.name + ' in his inventory.\n'
 def drop(self, name):
  if self.inventory.has_key(name):
   return self.inventory.pop(name)
 def say(self, what):
  return 'You says: ' + what + '.\n'
 def use(self, what):
  if self.inventory.has_key(what):
   return self.inventory[what].use()
  else:
   return 'You do not have ' + what + '.\n'

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

 def addObject(self, name, obj):
  if obj != None:
   self.objects[name] = obj
   return name + ' was dropped...\n'

 def getObject(self, name):
  if self.objects.has_key(name):
   return self.objects.pop(name)
  else:
   return 'There is no ' + name + ' around!\n'

 def touchObject(self, name):
  if self.objects.has_key(name):
   return self.objects[name].touch()
  else:
   return 'There is no ' + name + ' around!\n'

 def view(self, args = 'around'):
  if (args != '' and args != 'around'):
   try:
     return self.panorama[args].view()
   except KeyError:
     try:
      return self.objects[args].view()
     except KeyError:
      return 'nothing.'
  else:
   objects = []
   for v in self.objects.items():
    objects.append(v[0])
   objects = sorted(objects)
   for i in objects:
    if i[0] in ('a','e','i','o','u'):
     objects[objects.index(i)] = 'An ' + i + ' is here.'
    else:
     objects[objects.index(i)] = 'A ' + i + ' is here.'
   objectsStr = '\n'.join(objects)
   if (len(objects) >= 1):
    obsight = prcolor(3,'\n' + objectsStr)
   else:
    obsight = ''
   return self.sight + obsight

# CLASS COMMANDS ===============================================================
class SudCommand:
 """\n Available commands are:
 drop (d), exit (x), get (g), help (h), inventory (i), look (l), move (n,s,e,w),
 say (y), touch (t), use (u)

 For help with a specific command type "help command" or "h command". For
 example: type "help drop" without quotes to get help with drop command.\n"""
 def __init__(self, char, area):
  self.char = char
  self.area = area

 def drop(self, args):
  """\n DROP
 Drops item from inventory to current area.\n"""
  return self.area.addObject(args, self.char.drop(args))

 def d(self, args):
  """\n D
 Alias of drop.\n"""
  return self.drop(args)

 def exit(self, args):
  """\n EXIT (alias: x)
 Leave the game.\n"""
  print prcolor(5,'\n Bye, bye!\n')
  sys.exit()

 def x(self, args):
  """\n X
 Alias of exit.\n"""
  return self.exit(args)

 def get(self, args):
  """\n GET (alias: g)
 Takes an item from the ground. Requires an argument. Arguments should be the
 name of an item on the ground. \n"""
  try:
   return self.char.take(self.area.getObject(args))
  except AttributeError:
   return 'You cannot take ' + args + '.\n'

 def g(self, args):
  """\n G
 Alias of get.\n"""
  return self.get(args)

 def help(self, args):
  """\n HELP
 Gives you help in general or on a specific topic.\n"""
  if args == '':
   return self.__doc__
  else:
   try:
     return getattr(self, args).__doc__
   except AttributeError:
     return prcolor(1,'Help topic not found.\n')

 def h(self, args):
  """\n H
 Alias of help.\n"""
  return self.help(args)

 def inventory(self, args):
  """\n INVENTORY (alias: i)
 displays inventory.\n"""
  return self.char.name + ' has: ' + ', '.join(self.char.inventory)

 def i(self, args):
  """\n I
 Alias of inventory.\n"""
  return self.inventory(args)

 def look(self, args):
  """\n LOOK (alias: l)
 Show what you see when you look around.\n"""
  ClearScreen()
  return self.area.view(args) + '\n'

 def l(self, args):
  """\n L
 Alias of look.\n"""
  return self.look(args)

 def move(self, args):
  """\n MOVE (alias: n, s, e, w)
 Moves in some direction. Requires an argument. Arguments can be: north, south,
 east or west. Example: "move north" without quotes.\n"""
  area = self.area.relocate(args)
  if area != None:
   self.area = area
   return self.char.move(self.area)
  else:
   return 'There seems to be nothing that way.\n'

 def n(self, args):
  """\n N
 Alias of "move north".\n"""
  return self.move('north')

 def s(self, args):
  """\n S
 Alias of "move south".\n"""
  return self.move('south')

 def e(self, args):
  """\n E
 Alias of "move east".\n"""
  return self.move('east')

 def w(self, args):
  """\n W
 Alias of "move west".\n"""
  return self.move('west')

 def say(self, args):
  """\n SAY
 Makes character speak something. Requires an argument. Arguments should be
 what player wants his character to say. Example: "say kawabonga!" without
 quotes.\n"""
  return self.char.say(args)

 def y(self, args):
  """\n Y
 Alias of say.\n"""
  return self.say(args)

 def touch(self, args):
  """\n TOUCH
 Touches an item on the ground. Requires an argument. Arguments should be
 the name of an item on the ground.\n"""
  return self.area.touchObject(args)

 def t(self, args):
  """\n T
 Alias of touch.\n"""
  return self.touch(args)

 def use(self, args):
  """\n USE
 Uses an existing item inside character's inventory. Requires an argument.
 Arguments should be the name of an item inside character inventory.\n"""
  return self.char.use(args)

 def u(self, args):
  """\n U
 Alias of use.\n"""
  return self.use(args)

# CLASS GAME ===================================================================
class SudGame:
 def __init__(self, char, area):
  self.cmd = SudCommand(char, area)
  self.FirstSight = area.view() + '\n'

 def run(self):
  print self.FirstSight
  while True:
   command = raw_input('> ');
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
   result = prcolor(1,'Unknown command.\n')
  print result
