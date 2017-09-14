import unittest

import six

from braga import Entity, Component


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
        cat = Entity()

        catalive = Alive()
        cat.components.add(catalive)
        self.assertTrue(cat.has_component(Alive))

    def test_entity_attributes(self):
        cat = Entity()
        with self.assertRaises(AttributeError):
            cat.alive

        catalive = Alive()
        cat.components.add(catalive)

        self.assertTrue(cat.alive)

        cat.die()
        self.assertFalse(cat.alive)
        self.assertFalse(catalive.alive)

        cat.components.remove(catalive)

        with self.assertRaises(AttributeError):
            cat.resurrect()

    def test_entity_display(self):
        cat = Entity()
        display_str = '{}'
        if six.PY2:
            display_str = "Entity({}) - set([])"
        if six.PY3:
            display_str = "Entity({}) - set()"
        self.assertEqual(repr(cat), display_str.format(cat.uuid))

        catalive = Alive()
        cat.components.add(catalive)
        display_str = '{}'
        if six.PY2:
            display_str = "Entity({}) - set([Alive])".format(cat.uuid)
        if six.PY3:
            display_str = "Entity({})".format(cat.uuid) + " - {Alive}"

        self.assertEqual(repr(cat), display_str)

    def test_get_component(self):
        cat = Entity()
        catalive = Alive()
        cat.components.add(catalive)

        self.assertEqual(cat.get_component(Alive), catalive)
