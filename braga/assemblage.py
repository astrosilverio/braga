from braga.entity import Entity


class Assemblage(object):

    def __init__(self):
        self.component_types = dict()

    def add_component(self, component_type, init_args=None):
        self.component_types[component_type] = init_args

    def make(self):
        entity = Entity()
        entity.components |= set([k(v) if v is not None else k() for k, v in self.component_types.iteritems()])
        return entity
