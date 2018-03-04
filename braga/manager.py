from collections import defaultdict


class Manager(object):
    """Collates state for all instances of a given Component."""

    def __init__(self, component_type, properties_to_register=None):
        self.component_type = component_type
        self.entities_by_component = dict()

        if not properties_to_register:
            properties_to_register = self.component_type.INITIAL_PROPERTIES
        self.properties_to_register = properties_to_register

        for prop in self.properties_to_register:
            dict_name = "entities_by_{}".format(prop)
            setattr(self, dict_name, defaultdict(list))

    def register(self, entity):
        component = entity.get_component(self.component_type)
        self.entities_by_component[component] = entity

        for prop in self.properties_to_register:
            registry_name = "entities_by_{}".format(prop)
            registry = getattr(self, registry_name)
            registry[getattr(component, prop)].append(entity)
