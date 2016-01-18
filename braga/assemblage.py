from collections import defaultdict

from braga.entity import Entity


class Assemblage(object):

    def __init__(self, components=None):
        self.component_types = defaultdict(dict)
        if components and isinstance(components, dict):
            self.component_types.update(components)
        elif components and isinstance(components, list):
            for component in components:
                self.component_types[component]

    def add_component(self, component_type, **kwargs):
        self.component_types[component_type].update(**kwargs)

    def make(self, **kwargs):
        entity = Entity()
        for component_type, init_kwargs in self.component_types.iteritems():
            instance_kwargs = init_kwargs
            instance_kwargs.update({k:v for k,v in kwargs.iteritems() if k in component_type.INITIAL_PROPERTIES})

            component = component_type(**instance_kwargs)
            entity.components.add(component)

        return entity
