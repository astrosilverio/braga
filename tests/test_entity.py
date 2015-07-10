import unittest

from braga.models import Entity, Component


class Alive(Component):

    def __init__(self, alive=True):
        self._alive = alive

    @property
    def alive(self):
        return self._alive

    def die(self):
        self._alive = False

    def resurrect(self):
        self._alive = True


class TestEntity(unittest.TestCase):

    def test_has_component(self):
        cat = Entity(0)

        catalive = Alive()
        cat.components.add(catalive)
        self.assertTrue(cat.has_component(Alive))

    def test_entity_attributes(self):
        cat = Entity(0)
        with self.assertRaises(AttributeError):
            cat.alive

        catalive = Alive()
        cat.components.add(catalive)

        self.assertTrue(cat.alive)

        cat.die()
        self.assertFalse(cat.alive)

        cat.components.remove(catalive)

        with self.assertRaises(AttributeError):
            cat.resurrect()

    def test_entity_display(self):
        cat = Entity(0)
        self.assertEqual(repr(cat), "Entity(0) - set([])")

        catalive = Alive()
        cat.components.add(catalive)

        self.assertEqual(repr(cat), "Entity(0) - set([Alive])")
