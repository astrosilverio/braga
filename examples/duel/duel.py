from collections import defaultdict

from braga import Assemblage, Component, System, Aspect


#################################################
# Define components for players, rooms, and wand
#################################################
class Name(Component):  # for all entities

    INITIAL_PROPERTIES = ['name']

    def __init__(self, name=None):
        self.name = name


class Description(Component):  # for all entities

    INITIAL_PROPERTIES = ['description']

    def __init__(self, description=None):
        self.description = description


class Container(Component):
    pass


class Mappable(Component):
    def __init__(self, paths=None):
        self.paths = paths if paths else dict()


class Moveable(Component):

    INITIAL_PROPERTIES = ['location']

    def __init__(self, location=None):
        self.location = location


class Equipment(Component):

    INITIAL_PROPERTIES = ['equipment_type']

    def __init__(self, equipment_type):
        self.equipment_type = equipment_type


class Loyalty(Component):

    INITIAL_PROPERTIES = ['owner']

    def __init__(self, owner=None):
        self.owner = owner


class ExpelliarmusSkill(Component):
    def __init__(self):
        self.skill = 0


#####################################
# Define systems to manage components
#####################################
class ContainerSystem(System):
    def __init__(self, world, auto_update=False):
        super(ContainerSystem, self).__init__(world=world, aspect=Aspect(all_of=set([Container])))
        self.inventories = defaultdict(set)
        self.auto_update = auto_update
        for entity in self.world.entities_with_aspect(Aspect(all_of=set([Moveable]))):
            self.inventories[entity.location].add(entity)
        self.update()

    def update(self):
        for entity in self.world.entities_with_aspect(self.aspect):
            setattr(entity, 'inventory', self.inventories[entity])

    def move(self, thing, new_container, auto_update=False):
        if not thing.has_component(Moveable):
            raise ValueError("You cannot move this item")
        if not new_container in self.aspect:
            raise ValueError("Invalid destination")
        old_container = thing.location
        thing.location = new_container
        self.inventories[new_container].add(thing)
        if old_container:
            self.inventories[old_container].remove(thing)
        if auto_update or self.auto_update:
            self.update()


class EquipmentSystem(System):
    def __init__(self, world):
        super(EquipmentSystem, self).__init__(world=world, aspect=Aspect(all_of=set([Equipment])))
        self.equipment = defaultdict(lambda: None)

    def equip(self, bearer, item):
        if self.equipment[bearer]:
            raise ValueError("You cannot equip that at this time")
        self.equipment[bearer] = item
        setattr(bearer, item.equipment_type, item)

    def unequip(self, bearer, item):
        del self.equipment[bearer]
        delattr(bearer, item.equipment_type)

    def update(self):
        pass


#########################
# Define what a player is
#########################

player_factory = Assemblage(components=[Name, Description, Container, Moveable, ExpelliarmusSkill])

########################
# Define what a room is
########################

room_factory = Assemblage(components=[Name, Description, Container, Mappable])

#######################
# Define what a wand is
#######################

wand_factory = Assemblage(components={Name: {}, Equipment: {'equipment_type': 'wand'}, Moveable: {}, Loyalty: {}})
