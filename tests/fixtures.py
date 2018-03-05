from braga import Component


class Alive(Component):

    __slots__ = ['alive']

    def __init__(self, alive=True):
        self.alive = alive

    def die(self):
        self.alive = False

    def resurrect(self):
        self.alive = True


class Portable(Component):

    @property
    def is_portable(self):
        return True


class Container(Component):

    __slots__ = ['inventory']

    def __init__(self, inventory=None):
        self.inventory = set()
        if inventory:
            self.inventory |= inventory

    def pick_up(self, thing):
        if hasattr(thing, 'is_portable'):
            self.inventory.add(thing)

    def put_down(self, thing):
        self.inventory.remove(thing)


class Moveable(Component):

    __slots__ = ['v_x', 'v_y']

    def __init__(self, v_x=0, v_y=0):
        self.v_x = v_x
        self.v_y = v_y


class Location(Component):

    __slots__ = ['x', 'y']

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
