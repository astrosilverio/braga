from braga import Component


class Alive(Component):

    INITIAL_PROPERTIES = ['alive']

    def __init__(self, alive=True):
        self._alive = alive

    @property
    def alive(self):
        return self._alive

    def die(self):
        self._alive = False

    def resurrect(self):
        self._alive = True


class Portable(Component):

    @property
    def is_portable(self):
        return True


class Container(Component):

    INITIAL_PROPERTIES = ['inventory']

    def __init__(self, inventory=None):
        self._inventory = set()
        if inventory:
            self._inventory |= inventory

    @property
    def inventory(self):
        return self._inventory

    def pick_up(self, thing):
        if hasattr(thing, 'is_portable'):
            self._inventory.add(thing)

    def put_down(self, thing):
        self._inventory.remove(thing)


class Moveable(Component):

    INITIAL_PROPERTIES = ['v_x', 'v_y']

    def __init__(self, v_x=0, v_y=0):
        self.v_x = v_x
        self.v_y = v_y


class Location(Component):

    INITIAL_PROPERTIES = ['x', 'y']

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
