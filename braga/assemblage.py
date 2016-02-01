from collections import defaultdict

from braga import Entity


class Assemblage(object):
    """Factory for making Entities with particular combinations of Components."""

    def __init__(self, components=None):
        """ `components` can either be a list of Component classes
            or a dictionary, where the keys are
            Component classes and the values are dictionaries, where
            the key-value pairs are kwargs for the __init__ methods of the Component class
        """
        self.component_types = defaultdict(dict)
        if components and isinstance(components, dict):
            self.component_types.update(components)
        elif components and isinstance(components, list):
            for component in components:
                self.component_types[component]

    def add_component(self, component_type, **kwargs):
        self.component_types[component_type].update(**kwargs)

    def make(self, **kwargs):
        """ Makes an Entity with the Assemblage's combination of Components.

            Can initialize the Entity's components with particular values.
            If the Assemblage has been created with initial values for the parameters of its Components,
                those initial values are applied.
            If this method is called with kwargs, it will pass that initial value to the appropriate Component.
            Calling `make` with kwargs will override the initial values set on the Assemblage.

            Returns an Entity.
        """

        entity = Entity()

        for component_type, init_kwargs in self.component_types.iteritems():
            instance_kwargs = init_kwargs
            instance_kwargs.update({k:v for k,v in kwargs.iteritems() if k in component_type.INITIAL_PROPERTIES})

            component = component_type(**instance_kwargs)
            entity.components.add(component)

        return entity
