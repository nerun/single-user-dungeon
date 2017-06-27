# This file define what exists in the world.
from engine import *

# Objects (name, description, on touch, on use)
rose = MudObject('rose', 'a red blossom with spikes', 'bites fingers!', 'wanna eat it or what?')
shit = MudObject('shit', 'a stinky one', 'ewww...', 'you are sick, you know that?')
gaidys = MudObject('bird', 'oh, a cock!', 'looks like a rainbow', 'cuckarekoo! motherfucka!?!')

# Areas
woods = MudArea('deep green woods')
river = MudArea('shallow river')
hills = MudArea('orc hills')
house = MudArea('house of all gay')
meadow = MudArea('a green smelly meadow')

# Attaching interactive stuff to areas
river.addObject('object', shit)
woods.addObject('flower', rose)
woods.addObject('bird', gaidys)
meadow.addObject('animal', gaidys)

# Link all areas with bidirectional references
river.addArea('south', hills)
woods.addArea('north', river)
woods.addArea('west', house)
hills.addArea('east', meadow)
meadow.addArea('north', woods)

# Create a player
char = MudPlayer('spajus')

# Create a game with player and starting area
game = MudGame(char, woods)

# Lets go!
game.run()
