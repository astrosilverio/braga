from collections import defaultdict

import six

from braga import Entity


class Assemblage(object):
    """Factory for making Entities with particular combinations of Components."""

    def __init__(self, components, **kwargs):
        """ `components` can either be a list of Component classes
            or a dictionary, where the keys are
            Component classes and the values are dictionaries, where
            the key-value pairs are kwargs for the __init__ methods of the Component class
        """
        self.component_types = defaultdict(dict)
        for component in components:
            self.component_types[component].update(
                {k:v for k,v in six.iteritems(kwargs) if k in component.INITIAL_PROPERTIES}
            )
            kwargs = {k:v for k,v in six.iteritems(kwargs) if k not in component.INITIAL_PROPERTIES}

    def add_component(self, component_type, **kwargs):
        """Adds a component type to the factory."""
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

        for component_type, init_kwargs in six.iteritems(self.component_types):
            instance_kwargs = init_kwargs
            instance_kwargs.update({k:v for k,v in six.iteritems(kwargs) if k in component_type.INITIAL_PROPERTIES})
            kwargs = {k:v for k,v in six.iteritems(kwargs) if k not in component_type.INITIAL_PROPERTIES}

            component = component_type(**instance_kwargs)
            entity.components.add(component)

        if kwargs:
            raise ValueError("Unknown initial properties: {}".format(', '.join(six.iterkeys(kwargs))))

        return entity
