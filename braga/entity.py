import uuid


class Entity(object):
    """Represents a unique object."""

    def __init__(self):
        self._uuid = uuid.uuid4()
        self.components = set()

    @property
    def uuid(self):
        """Property to access the Entity's uuid, exists to prevent uuid modification."""
        return self._uuid

    def get_component(self, component_type):
        """ Retrives the component of a particular type belonging to this Entity.
            Raises an AttributeError if the Entity does not have a component of that class.
        """

        components = [comp for comp in self.components if isinstance(comp, component_type)]
        if not components:
            raise AttributeError
        else:
            return components[0]

    def has_component(self, component_type):
        """Determines if the Entity has a component of the given type."""
        return any(isinstance(comp, component_type) for comp in self.components)

    def __repr__(self):
        return "{0}({1}) - {2}".format(type(self).__name__, self._uuid, self.components)

    def __getattr__(self, name):
        """ Checks components for an attribute with a given name.
            Only raise an AttributeError if none of the Entity's components
            have an attribute with that name.
        """

        for component in self.components:
            try:
                attr = getattr(component, name)
            except AttributeError:
                pass
            else:
                return attr
        raise AttributeError
