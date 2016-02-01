class Aspect(object):
    """ Defines a pattern of Component types. Can be used to check if the set of components
        belonging to an Entity is consistent with the pattern.
    """

    def __init__(self, all_of=None, exclude=None, some_of=None):
        """ Defines the pattern of Components for this Aspect.
            :param all_of: Components that must be present
            :type all_of: set.
            :param exclude: Components that must not be present
            :type exclude: set.
            :param some_of: Components that may be present
            :type some_of: set.
        """
        self.all_of = all_of if all_of else set()
        self.exclude = exclude if exclude else set()
        self.some_of = some_of if some_of else set()

    def is_interested_in(self, entity):
        """ Determines if an Entity has Components consistent with the Aspect's pattern.
        :param entity: the Entity to evaluate
        :type entity: Entity.
        :returns: bool -- whether the Entity matches the Aspect
        """
        return (self._is_interested_in_all_of(entity) and
                self._is_interested_in_exclude(entity) and
                self._is_interested_in_some_of(entity))

    def __contains__(self, entity):
        """Syntactic sugar for `is_interested_in`."""
        return self.is_interested_in(entity)

    def _is_interested_in_all_of(self, entity):
        components = set([type(component) for component in entity.components])
        return components.issuperset(self.all_of)

    def _is_interested_in_exclude(self, entity):
        components = set([type(component) for component in entity.components])
        return not components & self.exclude

    def _is_interested_in_some_of(self, entity):
        components = set([type(component) for component in entity.components])
        return components & self.some_of or not self.some_of

    def select_entities(self, entities):
        return set([entity for entity in entities if self.is_interested_in(entity)])
