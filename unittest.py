import unittest
from engine import *

class TestMudObject(unittest.TestCase):
 def setUp(self):
  self.o = MudObject('object1', 'sight1', 'collision1', 'usage1')
  self.o2 = MudObject('object2', 'sight2')

 def test_view(self):
  self.assertEqual(self.o.view(), 'sight1')
  self.assertEqual(self.o2.view(), 'sight2')
  self.assertNotEqual(self.o.view(), 'c')
  self.assertNotEqual(self.o.view(), self.o2.view())

 def test_touch(self):
  self.assertEqual(self.o.touch(), 'collision1')
  self.assertEqual(self.o2.touch(), 'nothing happens')
  self.assertNotEqual(self.o.touch(), 'sight1')
  self.assertNotEqual(self.o.touch(), self.o2.touch())

 def test_use(self):
  self.assertEqual(self.o.use(), 'usage1')
  self.assertEqual(self.o2.use(), 'unusable')
  self.assertNotEqual(self.o.use(), 'unsuable')
  self.assertNotEqual(self.o.use(), self.o2.use())

class TestMudPlayer(unittest.TestCase):
 def setUp(self):
  self.p1 = MudPlayer('player1')
  self.p2 = MudPlayer('player2')
  self.area1 = MudArea('area1')
  self.area2 = MudArea('area2')
  self.o = MudObject('object1', 'sight1', 'collision1', 'usage1')
  self.o2 = MudObject('object2', 'sight2')

 def test_move(self):
  f1 = self.p1.move
  f2 = self.p2.move
  a1 = self.area1
  a2 = self.area2
  self.assertEqual(f1(a1), 'player1 moves to area1')
  self.assertEqual(f2(a1), 'player2 moves to area1')
  self.assertEqual(f1(a2), 'player1 moves to area2')
  self.assertEqual(f2(a2), 'player2 moves to area2')
  self.assertNotEqual(f1(a1), 'player1 moves to area2')

 def test_take_drop(self):
  take = self.p1.take
  use = self.p1.use
  drop = self.p1.drop
  inven = self.p1.inventory

  o1 = self.o
  o2 = self.o2

  self.assertEqual(inven, {})
  self.assertEqual(take(o1), 'player1 puts object1 in his inventory')
  self.assertEqual(inven, {'object1':o1})
  self.assertEqual(take(o2), 'player1 puts object2 in his inventory')
  self.assertEqual(inven, {'object1':o1, 'object2':o2})

  self.assertEqual(drop('object1'), o1)
  #neesamo objekto dropint neina
  self.assertRaises(TypeError, drop('object1'))
  self.assertEqual(inven, {'object2':o2})
  self.assertEqual(drop('object2'), o2)
  self.assertEqual(inven, {})

 def test_use(self):
  p1 = self.p1
  o1 = self.o
  self.assertNotEqual(p1.use('object1'), 'usage1')
  self.assertEqual(p1.use('object1'), 'you do not have object1')
  p1.take(o1)
  self.assertEqual(p1.use('object1'), 'usage1')

class TestMudArea(unittest.TestCase):
 def setUp(self):
  self.a1 = MudArea('area1')
  self.a2 = MudArea('area2')
  self.o1 = MudObject('obj1', 'sight1', 'collide1', 'use1')
  self.o2 = MudObject('obj2', 'sight2')

 def test_addArea(self):
  #Assignment must be mirrored
  self.a1.addArea('north', self.a2)
  self.assertEqual(self.a1.panorama, {'north':self.a2})
  self.assertEqual(self.a2.panorama, {'south':self.a1})

 def test_relocate(self):
  self.a1.addArea('north', self.a2)
  self.assertEqual(self.a1.relocate('north'), self.a2)
  self.assertEqual(self.a2.relocate('north'), None)
  self.assertEqual(self.a2.relocate('south'), self.a1)

 def test_addObject(self):
  self.assertEqual(self.a1.objects, {})
  #Dropped back because the object is usually added during the game when the player drops it.
  #A curly thing, but you will do it :)
  self.assertEqual(self.a1.addObject('something', self.o1), 'something was dropped..')
  self.assertEqual(self.a1.objects, {'something':self.o1})
  self.a1.addObject('other', self.o2)
  self.assertEqual(self.a1.objects, {'something':self.o1, 'other':self.o2})
  self.assertEqual(self.a1.addObject('something_clone', self.o1), 'something_clone was dropped..')
  self.assertEqual(self.a1.objects, {'something':self.o1, 'other':self.o2, 'something_clone':self.o1})

 def test_getObject(self):
  self.assertEqual(self.a1.objects, {})
  self.a1.addObject('something', self.o1)
  self.a1.addObject('other', self.o2)
  self.assertEqual(self.a1.getObject('something'), self.o1)
  self.assertEqual(self.a1.objects, {'other':self.o2})
  self.assertEqual(self.a1.getObject('something'), 'there is no something arround!')

 def test_touchObject(self):
  self.assertEqual(self.a1.objects, {})
  self.a1.addObject('something', self.o1)
  self.a1.addObject('other', self.o2)
  self.assertEqual(self.a1.touchObject('something'), self.o1.touch())
  self.assertNotEqual(self.a1.touchObject('obj2'), self.o2.touch())
  self.assertEqual(self.a1.touchObject('ass'), 'there is no ass arround!')

 def test_view(self):
  view = self.a1.view
  self.assertEqual(view(), 'area1')
  #unindentified object/panorama
  self.assertEqual(view('my brain'), 'nothing.')

  self.a1.addObject('my brain', self.o1)
  self.assertEqual(view('my brain'), self.o1.view())
  #Make you even more fun. Since I'm pride my brain, you have to show it.
  self.assertNotEqual(view(), 'area1')
  self.assertEqual(view(), 'area1. There also seems to be: my brain')
  self.a1.addObject('duck', self.o2)
  self.assertEqual(view(), 'area1. There also seems to be: my brain, duck') #', '.join(self.a1.objects)

  self.assertEqual(view('north'), 'nothing.')
  self.a1.addArea('north', self.a2)
  self.assertEqual(view('north'), 'area2')
  #Since the area2 should have been reflected and from there, looking southwards, should see area1 views.
  self.assertEqual(self.a2.view('south'), view())
  #Exactly. I see you :)

class MudCommandTest(unittest.TestCase):
 def setUp(self):
  self.p1 = MudPlayer('player1')
  self.a1 = MudArea('area1')
  self.a2 = MudArea('area2')
  self.o1 = MudObject('obj1', 'sight1', 'collide1', 'use1')
  self.o2 = MudObject('obj2', 'sight2', 'collide2', 'use2')
  self.a2.addObject('bread', self.o1)
  self.a2.addObject('pig', self.o2)
  self.a1.addArea('east', self.a2)
  self.c = MudCommand(self.p1, self.a1)

 def test_go_move(self):
  #MudArea.go === MudArea.move
  #test wrong way
  self.assertEqual(self.c.go('somewhere'), 'There seems to be nothing that way.')
  #test walk arround
  self.assertEqual(self.c.go('east'), 'player1 moves to area2')
  self.assertEqual(self.c.go('west'), 'player1 moves to area1')

 def test_use(self):
  self.assertEqual(self.c.use('bla'), 'you do not have bla')
  #lets go east and take something to test using
  self.c.go('east')
  self.c.take('bread')
  #as bread was only the looks, we know it's actually obj1, so lets use it
  self.assertEqual(self.c.use('obj1'), self.o1.use())

 def test_inventory(self):
  self.c.go('east')
  self.c.take('bread')
  self.assertEqual(self.c.inventory(None), 'player1 has: obj1')

 def test_help(self):
  self.assertEqual(self.c.help(''), self.c.__doc__)
  self.assertEqual(self.c.help('move'), self.c.move.__doc__)
  self.assertEqual(self.c.help('blabla'), 'help topic not found')

 def test_look(self):
  self.assertEqual(self.c.look(''), 'player1 sees ' + self.a1.view())
  self.assertEqual(self.c.look('at my balls'), 'player1 sees nothing.')
  self.assertEqual(self.c.look('east'), 'player1 sees ' + self.a2.view())

 def test_take(self):
  self.c.go('east')
  self.assertEqual(self.c.take('bread'), 'player1 puts obj1 in his inventory')
  self.assertEqual(self.p1.inventory, {'obj1':self.o1})
  #already taken!
  self.assertEqual(self.c.take('bread'), 'you cannot take bread')

 def test_touch(self): #perv test.. :)
  self.assertEqual(self.c.touch('self'), 'there is no self arround!')
  self.assertNotEqual(self.c.touch('bread'), self.o1.touch())
  self.c.go('east')
  #To touch is first to go
  self.assertEqual(self.c.touch('bread'), self.o1.touch())

 def test_drop(self):
  self.assertEqual(self.c.drop('smelly thing'), None)
  self.c.go('east')
  self.c.take('bread')
  self.c.go('west')
  self.assertEqual(self.c.drop('obj1'), 'obj1 was dropped..')
  self.assertEqual(self.a1.objects, {'obj1':self.o1})

 def test_say(self):
  self.assertEqual(self.c.say('i love this game'), 'player1 says: i love this game')
  self.assertNotEqual(self.c.say('python sucks'), 'player1 says: that\'s true!')

if __name__ == '__main__':
 unittest.main()
