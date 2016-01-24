from collections import defaultdict

from braga import Assemblage, Component, System, Aspect

#################################################
# define components for players, rooms, and wand
#################################################


class Name(Component):  # for all entities

    INITIAL_PROPERTIES = ['name']

    def __init__(self, name=None):
        self.name = name


class Description(Component):  # for all entities

    INITIAL_PROPERTIES = ['description']

    def __init__(self, description=None):
        self.description = description


class Container(Component):  # Container -- for room and player
    def __init__(self, inventory=None):
        self._inventory = inventory if inventory else set()

    @property
    def inventory(self):
        return self._inventory

    def add_entity(self, entity):
        self._inventory.add(entity)

    def remove_entity(self, entity):
        self._inventory.remove(entity)


class Mappable(Component):  # Mappable -- for room
    def __init__(self, paths=None):
        self.paths = paths if paths else dict()


class Moveable(Component):
    pass


class Equipment(Component):

    INITIAL_PROPERTIES = ['bearer', 'equipment_type']

    def __init__(self, equipment_type, bearer=None):
        self.bearer = bearer
        self.equipment_type = equipment_type


class Headgear(Component):

    INITIAL_PROPERTIES = ['bearer', 'equipment_type']

    def __init__(self, equipment_type, bearer=None):
        self.bearer = bearer
        self.equipment_type = equipment_type


class Footgear(Component):

    INITIAL_PROPERTIES = ['bearer', 'equipment_type']

    def __init__(self, equipment_type, bearer=None):
        self.bearer = bearer
        self.equipment_type = equipment_type


class BigEquipment(Equipment):

    INITIAL_PROPERTIES = ['bearer', 'equipment_type']

    def __init__(self, equipment_type, bearer=None):
        self.bearer = bearer
        self.equipment_type = equipment_type


class Loyalty(Component):

    INITIAL_PROPERTIES = ['owner']

    def __init__(self, owner=None):
        self.owner = owner


class ExpelliarmusSkill(Component):
    def __init__(self):
        self.skill = 0

# class AlohomoraSkill(Component):

#####################################
# define systems to manage components
#####################################


class DescriptionSystem(System):
    def __init__(self):
        super(DescriptionSystem, self).__init__(aspect=Aspect(all_of=set(Description)))

    def update(self):  # work this out later, rn have static descriptions
        pass


class ContainerSystem(System):
    def __init__(self):
        super(ContainerSystem, self).__init__(aspect=Aspect(all_of=set(Container)))

    def update(self):  # have it do sanity checks?
        pass

    def move(self, thing, new_container, old_container):
        thing.location = new_container
        new_container.add_entity(thing)
        old_container.remove_entity(thing)

    def print_inventory(self, container):
        pass


class EquipmentSystem(System):
    def __init__(self):
        # super(EquipmentSystem, self).__init__(aspect=Aspect(all_of=set(Equipment)))
        self.equipment = defaultdict(self.make_equipment_dict)

    def make_equipment_dict(self):
        return {'equipment': [], 'headgear': None, 'footgear': None}

    def equip(self, bearer, item):
        if not self.can_player_equip_item(bearer, item):
            raise ValueError("You cannot equip that at this time")
        setattr(bearer, item.equipment_type, item)
        if item.has_component(BigEquipment):
            self.equipment[bearer]['equipment'].append(item)
        if item.has_component(Equipment):
            self.equipment[bearer]['equipment'].append(item)
        else:
            self.equipment[bearer]['headgear'] = item
        bearer.equipment = self.equipment[bearer]

    def unequip(self, bearer, item):
        delattr(bearer, item.equipment_type)
        if item.has_component(BigEquipment):
            self.equipment[bearer]['equipment'].remove(item)
        if item.has_component(Equipment):
            self.equipment[bearer]['equipment'].remove(item)
        else:
            self.equipment[bearer]['headgear'] = None

    def update(self):
        pass

    def can_player_equip_item(self, bearer, item):
        if item.has_component(BigEquipment):
            return len(self.equipment[bearer]['equipment']) == 0
        if item.has_component(Equipment):
            return len(self.equipment[bearer]['equipment']) < 2
        else:
            return not self.equipment[bearer]['headgear']


# LoyaltySystem -- keeps track of what is loyal to who
# ExpelliarmusSkillSystem -- ??

#########################
# define what a player is
#########################

player_factory = Assemblage(components=[Name, Description, Container, Moveable, ExpelliarmusSkill])

########################
# define what a room is
########################

room_factory = Assemblage(components=[Name, Description, Container, Mappable])

#######################
# define what a wand is
#######################

wand_factory = Assemblage(components={Name: {}, Equipment: {'equipment_type': 'wand'}, Moveable: {}, Loyalty: {}})

################################################
# instatiate a room, two players, and two wands
################################################
