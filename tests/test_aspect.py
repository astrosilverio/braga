import unittest

from braga import Aspect, Entity
from tests.fixtures import Alive, Portable, Container, Moveable, Location


class TestAspect(unittest.TestCase):

    def setUp(self):
        self.cat = Entity()
        self.cat.components |= set([Alive(), Portable(), Container()])

        self.plant = Entity()
        self.plant.components.add(Alive())

        self.bathtub = Entity()
        self.bathtub.components.add(Container())

        self.brains = Entity()
        self.brains.components |= set([Portable(), Location()])

        self.zombie = Entity()
        self.zombie.components |= set([Moveable(), Location(), Container()])

        self.entities = set([self.cat, self.plant, self.bathtub, self.brains, self.zombie])

    def test_aspect_is_interested_in_all_of(self):
        aspect = Aspect(all_of=set([Alive, Portable]))

        self.assertTrue(aspect.is_interested_in(self.cat))
        self.assertFalse(aspect.is_interested_in(self.plant))
        self.assertFalse(aspect.is_interested_in(self.bathtub))
        self.assertFalse(aspect.is_interested_in(self.brains))
        self.assertFalse(aspect.is_interested_in(self.zombie))

        self.assertEqual(aspect.select_entities(self.entities), set([self.cat]))

    def test_aspect_is_interested_in_exclude(self):
        aspect = Aspect(exclude=set([Container]))

        self.assertFalse(aspect.is_interested_in(self.cat))
        self.assertTrue(aspect.is_interested_in(self.plant))
        self.assertFalse(aspect.is_interested_in(self.bathtub))
        self.assertTrue(aspect.is_interested_in(self.brains))
        self.assertFalse(aspect.is_interested_in(self.zombie))

        self.assertEqual(aspect.select_entities(self.entities), set([self.plant, self.brains]))

    def test_aspect_is_interested_in_some_of(self):
        aspect = Aspect(some_of=set([Location, Container]))

        self.assertTrue(aspect.is_interested_in(self.cat))
        self.assertFalse(aspect.is_interested_in(self.plant))
        self.assertTrue(aspect.is_interested_in(self.bathtub))
        self.assertTrue(aspect.is_interested_in(self.brains))
        self.assertTrue(aspect.is_interested_in(self.zombie))

        self.assertEqual(aspect.select_entities(self.entities), set([self.cat, self.bathtub, self.brains, self.zombie]))

    def test_aspect_is_interested_in_different_categories(self):
        aspect = Aspect(all_of=set([Container]), exclude=set([Moveable]), some_of=set([Location, Portable, Alive]))

        self.assertTrue(aspect.is_interested_in(self.cat))
        self.assertFalse(aspect.is_interested_in(self.plant))
        self.assertFalse(aspect.is_interested_in(self.bathtub))
        self.assertFalse(aspect.is_interested_in(self.brains))
        self.assertFalse(aspect.is_interested_in(self.zombie))

        self.assertEqual(aspect.select_entities(self.entities), set([self.cat]))
