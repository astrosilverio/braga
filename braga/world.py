from braga.entity import Entity


class World(object):
    """Collects all the Entities for a particular program."""

    def __init__(self):
        self.entities = set()

    def entities_with_aspect(self, aspect):
        """Returns a set of Entities in the World with a particular Aspect."""
        return set([entity for entity in self.entities if entity in aspect])

    def make_entity(self, assemblage=None, **kwargs):
        """ Creates an Entity for this World.
            :param assemblage: Assemblage the Entity should be built with
            :type assemblage: Assemblage.

            Can take kwargs that will be passed to the assemblage's `make` method.

            Returns an Entity.
        """

        if not assemblage:
            new_entity = Entity()
        else:
            new_entity = assemblage.make(**kwargs)

        self.entities.add(new_entity)
        return new_entity
