from game.libraries import *

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
            if self.inventory[name]["quantity"] > 1:
                self.inventory[name]["quantity"] -= 1
                return self.inventory[name]["object"]
            else:
                return self.inventory.pop(name)["object"]

    def move(self, area):
        clear()
        return area.view()

    def say(self, what):
        return engine["you_says"] % (what) + '\n'

    def status(self, args):
        status = engine["char_sheet"] % (self.name, self.ST, self.DX, self.IQ, self.HT)
        return status

    def take(self, obj):
        if obj.name in self.inventory:
            self.inventory[obj.name]["quantity"] += 1
        else:
            self.inventory[obj.name] = {"object": obj, "quantity": 1}
        return engine["placed_inventory"] % (obj.name) + "\n"

    def touch(self, name):
        if name in self.inventory:
            return self.inventory[name]["object"].touch()

    def use(self, what):
        if what in self.inventory:
            return self.inventory[what]["object"].use()
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
        return self.panorama.get(args, None)

    def addObject(self, obj):
        if obj is not None:
            if obj.name in self.objects:
                self.objects[obj.name]["quantity"] += 1
            else:
                self.objects[obj.name] = {"object": obj, "quantity": 1}
            return engine["item_was_dropped"] % (obj.name) + "\n"

    def getObject(self, name):
        if name in self.objects:
            if self.objects[name]["quantity"] > 1:
                self.objects[name]["quantity"] -= 1
                return self.objects[name]["object"]
            else:
                return self.objects.pop(name)["object"]
        else:
            return engine["there_isnt_around"] % (name) + "\n"

    def touchObject(self, name):
        if name in self.objects:
            return self.objects[name]["object"].touch()
        else:
            return engine["there_isnt_around"] % (name) + "\n"

    def view(self, args='around'):
        if args and args != 'around':
            if args in self.panorama:
                return self.panorama[args].view()
            elif args in self.objects:
                return self.objects[args]["object"].view()
            else:
                return engine["there_isnt_around"] % (args) + "\n"
        else:
            if not self.objects:
                return self.sight

            objects_list = []
            for name, data in sorted(self.objects.items()):
                qty = data["quantity"]
                if qty > 1:
                    item_desc = f"{name} ({qty})"
                else:
                    item_desc = name

                article = engine["an_item_is_here"] if item_desc[0].lower() in 'aeiou' else engine["a_item_is_here"]
                objects_list.append(article % item_desc)

            obsight = span('\n' + '\n'.join(objects_list), 'yellow')
            return self.sight + obsight


# CLASS COMMANDS ===============================================================
class SudCommand:
    __doc__ = "\n " + engine["available_commands"] + "\n"
    
    def __init__(self, char, area):
        self.char = char
        self.area = area

        # Map aliases to real methods
        self.aliases = {
            'd': self.drop,
            'x': self.exit,
            'quit': self.exit,
            'q': self.exit,
            'g': self.get,
            'h': self.help,
            'i': self.inventory,
            'l': self.look,
            'n': lambda args: self.move('north'),
            's': lambda args: self.move('south'),
            'e': lambda args: self.move('east'),
            'w': lambda args: self.move('west'),
            'y': self.say,
            'st': self.status,
            't': self.touch,
            'u': self.use
        }

    def __getattr__(self, name):
        if name in self.aliases:
            return self.aliases[name]
        raise AttributeError(f"'SudCommand' object has no attribute '{name}'")

    def drop(self, args):
        return self.area.addObject(self.char.drop(args))
    drop.__doc__ = "\n " + engine["drop"] + "\n"

    def exit(self, args):
        print(span("\n " + engine["bye"]  + "\n", 'magenta'))
        exit()
    exit.__doc__ = "\n " + engine["exit"] + "\n"

    def get(self, args):
        try:
            return self.char.take(self.area.getObject(args))
        except AttributeError:
            return engine["cant_take"] + ' ' + args + '.\n'
    get.__doc__ = "\n " + engine["get"] + "\n"

    def help(self, args):
        if args == '':
            return self.__doc__
        else:
            try:
                return getattr(self, args).__doc__
            except AttributeError:
                return span(engine["help_topic_not_found"], 'red') + "\n\n " + engine["available_commands"] + "\n"
    help.__doc__ = "\n " + engine["help"] + "\n"

    def inventory(self, args):
        if self.char.inventory:
            inv_list = [f"{name} ({data['quantity']})" if data["quantity"] > 1 else name 
                        for name, data in self.char.inventory.items()]
            return engine["your_inventory"] + ':\n - ' + '\n - '.join(inv_list) + '\n'
        else:
            return engine["inventory_empty"] + "\n"
    inventory.__doc__ = "\n " + engine["inventory"] + "\n"

    def look(self, args):
        if args == "":
            clear()
        return self.area.view(args)
    look.__doc__ = "\n " + engine["look"] + "\n"

    def move(self, args):
        area = self.area.relocate(args)
        if area is not None:
            self.area = area
            return self.char.move(self.area)
        else:
            return engine["nothing_that_way"] + "\n"
    move.__doc__ = "\n " + engine["move"] + "\n"

    def say(self, args):
        return self.char.say(args)
    say.__doc__ = "\n " + engine["say"] + "\n"

    def status(self, args):
        return self.char.status(args)
    status.__doc__ = "\n " + engine["status"] + "\n"

    def touch(self, args):
        if args in self.char.inventory:
            return self.char.touch(args)
        else:
            return self.area.touchObject(args)
    touch.__doc__ = "\n " + engine["touch"] + "\n"

    def use(self, args):
        return self.char.use(args)
    use.__doc__ = "\n " + engine["use"] + "\n"


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
            result = span(engine["unknown_command"], 'red') + "\n\n " + engine["available_commands"] + "\n"
        
        print(result)
