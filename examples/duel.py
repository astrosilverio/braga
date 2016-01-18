from braga import Assemblage, Component, System, Aspect

#################################################
# define components for players, rooms, and wand
#################################################

class Description(Component):  # for all entities
    def __init__(self, description=None):
        self.description = description


class Container(Component): # Container -- for room and player
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


class Moveable(Component):  # Moveable -- for player and wand
    def __init__(self, location=None):
        self.location = location

    @property
    def is_moveable(self):
        return True


class Equipment(Component):  # Equipment -- for wand
    def __init__(self, bearer=None, equipment_type=None):
        self.bearer = bearer
        self.equipment_type = equipment_type


# Loyalty -- for wand
# ExpelliarmusSkill -- for player

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
        if not thing.is_moveable:
            raise TypeError("Item is not movable")
        thing.location = new_container
        new_container.add_entity(thing)
        old_container.remove_entity(thing)

    def print_inventory(self, container):
        pass

# MappableSystem -- keeps track of how rooms are connected?
# MoveableSystem -- keeps track of who holds things?


class EquipmentSystem(System):
    def __init__(self):
        super(EquipmentSystem, self).__init__(aspect=Aspect(all_of=set(Equipment)))
        self.equipment = defaultdict(dict)

    def equip(self, bearer, item):
        setattr(bearer, item.equipment_type, item)
        self.equipment[bearer][item.equipment_type] = item

    def unequip(self, bearer, item):
        delattr(bearer, item.equipment_type)
        del self.equipment[bearer][item.equipment_type]

    def update(self):
        pass


# LoyaltySystem -- keeps track of what is loyal to who
# ExpelliarmusSkillSystem -- ??

#########################
# define what a player is
#########################
player_factory = Assemblage()

########################
# define what a room is
########################

#######################
# define what a wand is
#######################

################################################
# instatiate a room, two players, and two wands
################################################