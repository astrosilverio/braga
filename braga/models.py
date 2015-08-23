import abc
import threading
import uuid


class Entity(object):

    def __init__(self):
        self._uuid = uuid.uuid4()
        self.components = set()

    @property
    def uuid(self):
        return self._uuid

    def has_component(self, component_type):
        return any(isinstance(comp, component_type) for comp in self.components)

    def __repr__(self):
        return "{0}({1}) - {2}".format(type(self).__name__, self._uuid, self.components)

    def __getattr__(self, name):
        for component in self.components:
            try:
                attr = getattr(component, name)
            except AttributeError:
                pass
            else:
                return attr
        raise AttributeError


class Component(object):
    def __repr__(self):
        return type(self).__name__


class Assemblage(object):

    def __init__(self):
        self.component_types = dict()

    def add_component(self, component_type, init_args=None):
        self.component_types[component_type] = init_args

    def make(self):
        entity = Entity()
        entity.components |= set([k(v) if v is not None else k() for k, v in self.component_types.iteritems()])
        return entity


class System(object):

    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self.thread = None

    def start(self):
        self.thread = threading.Thread(name=type(self).__name__, target=self.update)
        self.thread.start()

    @abc.abstractmethod
    def update(self):
        """Updates the entities in this system"""
