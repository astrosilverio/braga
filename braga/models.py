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

    def __init__(self, aspect=None):
        self.thread = None
        self.aspect = aspect if aspect else Aspect()

    def start(self):
        self.thread = threading.Thread(name=type(self).__name__, target=self.update)
        self.thread.start()

    @abc.abstractmethod
    def update(self):
        """Updates the entities in this system"""


class Aspect(object):

    def __init__(self, all_of=None, exclude=None, some_of=None):
        self.all_of = all_of if all_of else set()
        self.exclude = exclude if exclude else set()
        self.some_of = some_of if some_of else set()

    def is_interested_in(self, entity):
        return (self.is_interested_in_all_of(entity) and
                self.is_interested_in_exclude(entity) and
                self.is_interested_in_some_of(entity))

    def is_interested_in_all_of(self, entity):
        components = set([type(component) for component in entity.components])
        return components.issuperset(self.all_of)

    def is_interested_in_exclude(self, entity):
        components = set([type(component) for component in entity.components])
        return not components & self.exclude

    def is_interested_in_some_of(self, entity):
        components = set([type(component) for component in entity.components])
        return components & self.some_of or not self.some_of

    def select_entities(self, entities):
        return set([entity for entity in entities if self.is_interested_in(entity)])
