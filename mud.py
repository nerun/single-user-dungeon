# -*- coding: cp860 -*-
# This file define what exists in the world.
import os
from engine import *

# Create subdirectory "rooms" if it do not exist
if os.path.isdir('./rooms') is False:
 os.mkdir('./rooms')

# Objects (name, description, on touch, on use)
rose = MudObject('rose', 'a red blossom with thorns.', 'the thorns hurt your finger!', 'you wear it to adorn your clothes.')
poo = MudObject('poo', 'stinky and brown.', 'it looks soft, brown and definitely disgusting.', 'you are sick, you know that?')
sparrow = MudObject('sparrow', 'small with thick beak and brown color.', 'it looks delicate.', 'tweet! Tweet!')
apple = MudObject('apple', 'a red fruit the size of a closed fist.', 'hard but not so, and smooth.', 'hmmm delicious!')

# Areas
port = MudArea(prcolor(6,'Port Codfish\n')+'[ Exits: n s w ]')
beach = MudArea(prcolor(6,'Drowned man beach\n')+'[ Exits: s ]')
village = MudArea(prcolor(6,'Boot fishers village\n')+'[ Exits: e ]')
house = MudArea(prcolor(6,'Customhouse\n')+'[ Exits: e ]')
maiden = MudArea(prcolor(6,'Raped maiden beach\n')+'[ Exits: n w ]')

# Attaching interactive stuff to areas
beach.addObject('crap', poo)
port.addObject('flower', rose)
port.addObject('fruit', apple)
maiden.addObject('bird', sparrow)

# Link all areas with bidirectional references
port.addArea('north', beach)
port.addArea('west', house)
village.addArea('east', maiden)
maiden.addArea('north', port)

# Create a player
char = MudPlayer('Player')

# Create a game with player and starting area
game = MudGame(char, port)

# Lets go!
ClearScreen()
game.run()
