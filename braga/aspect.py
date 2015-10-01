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
