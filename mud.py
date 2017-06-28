# This file define what exists in the world.
from engine import *

# Objects (name, description, on touch, on use)
rose = MudObject('rose', 'a red blossom with spikes.', 'bites fingers!', 'wanna eat it or what?')
shit = MudObject('shit', 'a stinky one.', 'yuck...', 'you are sick, you know that?')
cock = MudObject('bird', 'oh, a cock!', 'looks like a rainbow.', 'tweet!')
apple = MudObject('apple', 'a red fruit the size of a closed fist.', 'hard but not so, and smooth.', 'hmmm delicious!')

# Areas
woods = MudArea(prcolor(6,'Deep green woods\n')+'[ Exits: n s w ]')
river = MudArea(prcolor(6,'Shallow river\n')+'[ Exits: s ]')
hills = MudArea(prcolor(6,'Orc hills\n')+'[ Exits: e ]')
house = MudArea(prcolor(6,'House of all gay\n')+'[ Exits: e ]')
meadow = MudArea(prcolor(6,'A green smelly meadow\n')+'[ Exits: n w ]')

# Attaching interactive stuff to areas
river.addObject('object', shit)
woods.addObject('flower', rose)
woods.addObject('bird', cock)
woods.addObject('apple', apple)
meadow.addObject('sparrow', cock)

# Link all areas with bidirectional references
woods.addArea('north', river)
woods.addArea('west', house)
hills.addArea('east', meadow)
meadow.addArea('north', woods)

# Create a player
char = MudPlayer('Player')

# Create a game with player and starting area
game = MudGame(char, woods)

# Lets go!
ClearScreen()
game.run()
