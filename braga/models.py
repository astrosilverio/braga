class Entity(object):

    def __init__(self, uuid):
        self._uuid = uuid
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
