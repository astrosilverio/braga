import abc
import threading

from braga.aspect import Aspect


class System(object):
    """Handler for modifying and updating Entities with a particular pattern of Components."""

    __metaclass__ = abc.ABCMeta

    def __init__(self, world, aspect=None):
        self.thread = None
        self.world = world
        self.aspect = aspect if aspect else Aspect()

    def start(self):
        self.thread = threading.Thread(name=type(self).__name__, target=self.update)
        self.thread.start()

    def __contains__(self, entity):
        return entity in self.aspect

    @property
    def entities(self):
        """Set of Entities in the World with this Aspect"""
        return self.world.entities_with_aspect(self.aspect)

    @abc.abstractmethod
    def update(self):
        """Updates the entities in this system"""
