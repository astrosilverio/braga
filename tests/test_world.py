import unittest

from braga import World, Entity, Assemblage, System
from tests.fixtures import Moveable, Location


class SomeKindOfSystem(System):

    def __init__(self, world):
        super(SomeKindOfSystem, self).__init__(world=world)

    def do_something(self, thing):
        pass

    def update(self):
        pass


class TestWorld(unittest.TestCase):

    def setUp(self):
        self.world = World()

    def test_make_entity_without_assemblage_makes_entity(self):
        new_entity = self.world.make_entity()

        self.assertTrue(isinstance(new_entity, Entity))
        self.assertIn(new_entity, self.world.entities)
        self.assertEqual(new_entity.components, set())

    def test_make_entity_with_assemblage_makes_entity(self):
        new_entity = self.world.make_entity(Assemblage([Moveable, Location]))

        self.assertTrue(isinstance(new_entity, Entity))
        self.assertIn(new_entity, self.world.entities)
        self.assertTrue(new_entity.has_component(Moveable))
        self.assertTrue(new_entity.has_component(Location))

    def test_make_entity_with_initial_properties(self):
        new_entity = self.world.make_entity(Assemblage([Moveable, Location]), x=1, v_y=2)

        self.assertTrue(isinstance(new_entity, Entity))
        self.assertIn(new_entity, self.world.entities)
        self.assertTrue(new_entity.has_component(Moveable))
        self.assertTrue(new_entity.has_component(Location))

        self.assertEqual(new_entity.x, 1)
        self.assertEqual(new_entity.v_y, 2)

    def test_destroy_entity_removes_entity_from_world(self):
        new_entity = self.world.make_entity()
        self.assertIn(new_entity, self.world.entities)

        self.world.destroy_entity(new_entity)
        self.assertNotIn(new_entity, self.world.entities)

    def test_destroy_entity_raises_if_not_entity(self):
        unrelated_entity = Entity()
        self.assertNotIn(unrelated_entity, self.world.entities)

        with self.assertRaises(ValueError) as e:
            self.world.destroy_entity(unrelated_entity)

        self.assertEqual(e.exception.message, "{0} does not contain {1}".format(repr(self.world), repr(unrelated_entity)))

    def test_add_system_registers_system(self):
        new_system = self.world.add_system(SomeKindOfSystem)

        self.assertTrue(isinstance(new_system, System))
        self.assertEqual(new_system, self.world.systems[SomeKindOfSystem])
        self.assertEqual(new_system.world, self.world)

    def test_add_system_rejects_non_systems(self):
        with self.assertRaises(ValueError) as e:
            self.world.add_system(Assemblage)

        self.assertEqual(e.exception.message, "{} is not a type of System".format(Assemblage.__name__))

    def test_add_system_rejects_duplicate_systems(self):
        self.world.add_system(SomeKindOfSystem)

        with self.assertRaises(ValueError) as e:
            self.world.add_system(SomeKindOfSystem)

        self.assertEqual(e.exception.message, "World already contains a System of type {}".format(repr(SomeKindOfSystem)))

    def test_can_subscribe_functions_to_systems(self):
        def check_to_run_before_method(system, thing):
            pass

        def check_to_run_after_method(system, thing):
            pass

        system = self.world.add_system(SomeKindOfSystem)

        self.world.subscribe(system, 'do_something', check_to_run_before_method, before=True)
        self.world.subscribe(system, 'do_something', check_to_run_after_method, after=True)

        self.assertIn(check_to_run_before_method, self.world.subscriptions[system]['do_something']['before'])
        self.assertIn(check_to_run_after_method, self.world.subscriptions[system]['do_something']['after'])

    def test_cannot_subscribe_non_functions_to_systems(self):
        system = self.world.add_system(SomeKindOfSystem)

        for thing in ['string', [], {}, system]:
            with self.assertRaises(TypeError):
                self.world.subscribe(system, 'do_something', thing)
