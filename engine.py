import sys

class MudObject:
 def __init__(self, name, sight, collide = 'nothing happens', usability = 'unusable'):
  self.name = name
  self.sight = sight
  self.collide = collide
  self.usability = usability
 def view(self):
  return self.sight
 def touch(self):
  return self.collide
 def use(self):
  return self.usability

class MudPlayer:
 def __init__(self, name):
  self.inventory = {}
  self.name = name
  self.health = 100
 def move(self, area):
  return self.name + ' moves to ' + area.sight
 def take(self, obj):
  self.inventory[obj.name] = obj
  return self.name + ' puts ' + obj.name + ' in his inventory'
 def drop(self, name):
  if self.inventory.has_key(name):
   return self.inventory.pop(name)
 def say(self, what):
  return self.name + ' says: ' + what
 def use(self, what):
  if self.inventory.has_key(what):
   return self.inventory[what].use()
  else:
   return 'you do not have ' + what

class MudArea:
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
   return name + ' was dropped..'
 def getObject(self, name):
  if self.objects.has_key(name):
   return self.objects.pop(name)
  else:
   return 'there is no ' + name + ' arround!'
 def touchObject(self, name):
  if self.objects.has_key(name):
   return self.objects[name].touch()
  else:
   return 'there is no ' + name + ' arround!'
 def view(self, args = 'arround'):
  if (args != '' and args != 'arround'):
   try:
     return self.panorama[args].view()
   except KeyError:
     try:
      return self.objects[args].view()
     except KeyError:
      return 'nothing.'
  else:
   objects = ', '.join([k for k, v in self.objects.items()])
   if (objects != ''):
    obsight = '. There also seems to be: ' + objects
   else:
    obsight = ''
   return self.sight + obsight

class MudCommand:
 """ welcome to mud. available commands are:
 go, move, help, exit, look, touch, say, take, drop, inventory, use """
 def __init__(self, char, area):
  self.char = char
  self.area = area

 def go(self, args):
  """ alias of move """
  return self.move(args)

 def use(self, args):
  """ uses item from inventory """
  return self.char.use(args)

 def inventory(self, args):
  """ displays inventory """
  return self.char.name + ' has: ' + ', '.join(self.char.inventory)

 def help(self, args):
  """ gives you help on a topic"""
  if args == '':
   return self.__doc__
  else:
   try:
     return getattr(self, args).__doc__
   except AttributeError:
     return 'help topic not found'

 def exit(self, args):
  """ exits game """
  print 'bye bye!'
  sys.exit()

 def look(self, args):
  """ lets you look arround """
  return self.char.name + ' sees ' + self.area.view(args)

 def take(self, args):
  """ takes item from the ground """
  try:
   return self.char.take(self.area.getObject(args))
  except AttributeError:
   return 'you cannot take ' + args

 def touch(self, args):
  """ touches item from the ground """
  return self.area.touchObject(args)

 def drop(self, args):
  """ drops item from inventory to current area """
  return self.area.addObject(args, self.char.drop(args))

 def move(self, args):
  """ moves arround """
  area = self.area.relocate(args)
  if area != None:
   self.area = area
   return self.char.move(self.area)
  else:
   return 'There seems to be nothing that way.'

 def say(self, args):
  """ makes character talk """
  return self.char.say(args)

class MudGame:
 def __init__(self, char, area):
  self.cmd = MudCommand(char, area)

 def run(self):
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
   result = 'Unknown Command'
  print result
