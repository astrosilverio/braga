from collections import defaultdict

from braga.entity import Entity
from braga.system import System


class World(object):
    """Collects all the Entities for a particular program."""

    def __init__(self):
        self.entities = set()
        self.systems = defaultdict(lambda: None)
        self.timer = 0
        self.subscriptions = defaultdict(lambda: defaultdict(lambda: {'after': [], 'before': []}))

    def refresh(self):
        for system in self.systems.values():
            system.update()

    def step(self):
        self.timer += 1

    def entities_with_aspect(self, aspect):
        """Returns a set of Entities in the World with a particular Aspect."""
        return set([entity for entity in self.entities if entity in aspect])

    def make_entity(self, assemblage=None, **kwargs):
        """ Creates an Entity for this World.
            :param assemblage: Assemblage the Entity should be built with
            :type assemblage: Assemblage.

            Can take kwargs that will be passed to the assemblage's `make` method.

            Returns an Entity.
        """

        if not assemblage:
            new_entity = Entity()
        else:
            new_entity = assemblage.make(**kwargs)

        self.entities.add(new_entity)
        return new_entity

    def destroy_entity(self, entity):
        """Removes entity from the world."""
        try:
            self.entities.remove(entity)
        except KeyError:
            raise ValueError("{0} does not contain {1}".format(repr(self), repr(entity)))

    def add_system(self, system_type):
        """ Creates a System for this World.
            :param system_type: user-defined System class that the new System should be an instance of
            :type system_type: System

            Returns a System.
        """

        if not issubclass(system_type, System):
            raise ValueError("{} is not a type of System".format(system_type.__name__))
        if self.systems[system_type]:
            raise ValueError("World already contains a System of type {}".format(repr(system_type)))

        new_system = system_type(world=self)
        self.systems[system_type] = new_system

        return new_system

    def publish(self, event, *involved_entities):
        """Publishes an event to the World."""
        callbacks = self.subscriptions[event]
        extra_output = '\n'.join([callback(*involved_entities) for callback in callbacks])
        self.step()
        return extra_output

    def subscribe(self, system, method, callback, before=False, after=False):
        if not (before or after):
            raise ValueError("You won't actually subscribe anything to anything unless you set before or after")

        if not hasattr(callback, '__call__'):
            raise TypeError("Only callables can be registered as preactions or reactions")

        if before:
            self.subscriptions[system][method]['before'].append(callback)
        if after:
            self.subscriptions[system][method]['after'].append(callback)
