import unittest

import six

from braga import Entity, Assemblage, World
from tests.fixtures import Alive, Portable, Container


class TestAssemblage(unittest.TestCase):

    def setUp(self):
        self.world = World()

        self.human = Entity()
        self.human.components.add(Container())

        self.food = Entity()
        self.food.components.add(Portable())

    def test_assemblage_makes_entity(self):
        cat_factory = Assemblage([Alive, Portable])
        cat = cat_factory.make()

        self.assertTrue(isinstance(cat, Entity))
        self.assertTrue(cat.alive)
        self.assertTrue(cat.is_portable)

    def test_assembled_entity_interacts_normally(self):
        cat_factory = Assemblage([Alive, Portable, Container])
        cat = cat_factory.make()

        # pick up cat
        self.human.pick_up(cat)
        self.assertIn(cat, self.human.inventory)

        # feed cat
        cat.pick_up(self.food)
        self.assertIn(self.food, cat.inventory)

    def test_assembling_entity_with_initial_conditions(self):
        zombie_cat_factory = Assemblage([Alive], alive=False)
        zombie_cat = zombie_cat_factory.make()
        self.assertFalse(zombie_cat.alive)
        zombie_cat.resurrect()
        self.assertTrue(zombie_cat.alive)

        fed_cat_factory = Assemblage([Container], inventory=set([self.food]))
        fed_cat = fed_cat_factory.make()
        self.assertEqual(self.food.uuid, fed_cat.inventory.pop().uuid)

    def test_assembled_cats_are_independent(self):
        cat_factory = Assemblage([Alive, Portable])

        my_cat = cat_factory.make()
        stray_cat = cat_factory.make()
        self.human.pick_up(my_cat)

        self.assertNotEqual(my_cat.uuid, stray_cat.uuid)
        self.assertIn(my_cat, self.human.inventory)
        self.assertNotIn(stray_cat, self.human.inventory)

    def test_adding_component_with_initial_components(self):
        cat_factory = Assemblage(components=[Portable])
        cat_factory.add_component(Alive)
        cat = cat_factory.make()

        self.assertTrue(isinstance(cat, Entity))
        self.assertTrue(cat.alive)
        self.assertTrue(cat.is_portable)

    def test_initializing_components_at_production_time(self):
        cat_factory = Assemblage(components=[Alive, Portable])
        zombie_cat = cat_factory.make(alive=False)

        self.assertTrue(isinstance(zombie_cat, Entity))
        self.assertFalse(zombie_cat.alive)
        self.assertTrue(zombie_cat.is_portable)

    def test_unknown_initial_properties_at_production_time(self):
        cat_factory = Assemblage(components=[Alive, Portable])

        with self.assertRaises(ValueError) as e:
            cat_factory.make(live=True, aliv=True)  # misspell some properties

        if six.PY2:
            exception_message = e.exception.message
        if six.PY3:
            exception_message = str(e.exception)

        self.assertEqual(exception_message, "Unknown initial properties: live, aliv")
