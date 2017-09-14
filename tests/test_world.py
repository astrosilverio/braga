import unittest

import six

from braga import World, Entity, Assemblage, System
from tests.fixtures import Moveable, Location


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

        if six.PY2:
            exception_message = e.exception.message
        if six.PY3:
            exception_message = str(e.exception)

        self.assertEqual(exception_message, "{0} does not contain {1}".format(repr(self.world), repr(unrelated_entity)))

    def test_add_system_registers_system(self):
        self.skipTest('Functionality soon to be removed')
        new_system = self.world.add_system(SomeKindOfSystem)

        self.assertTrue(isinstance(new_system, System))
        self.assertEqual(new_system, self.world.systems[SomeKindOfSystem])
        self.assertEqual(new_system.world, self.world)

    def test_add_system_rejects_non_systems(self):
        self.skipTest('Functionality soon to be removed')
        with self.assertRaises(ValueError) as e:
            self.world.add_system(Assemblage)

        self.assertEqual(e.exception.message, "{} is not a type of System".format(Assemblage.__name__))

    def test_add_system_rejects_duplicate_systems(self):
        self.skipTest('Functionality soon to be removed')
        self.world.add_system(SomeKindOfSystem)

        with self.assertRaises(ValueError) as e:
            self.world.add_system(SomeKindOfSystem)

        self.assertEqual(e.exception.message, "World already contains a System of type {}".format(repr(SomeKindOfSystem)))

    def test_can_subscribe_functions_to_systems(self):
        def check_to_run_before_method(system, thing):
            pass

        def check_to_run_after_method(system, thing):
            pass

        some_kind_of_system = System(self.world)

        self.world.subscribe(some_kind_of_system, 'do_something', check_to_run_before_method, before=True)
        self.world.subscribe(some_kind_of_system, 'do_something', check_to_run_after_method, after=True)

        self.assertIn(check_to_run_before_method, self.world.subscriptions[some_kind_of_system]['do_something']['before'])
        self.assertIn(check_to_run_after_method, self.world.subscriptions[some_kind_of_system]['do_something']['after'])

    def test_cannot_subscribe_non_callables_to_systems(self):
        class Foo(object):
            pass

        foo = Foo()
        some_kind_of_system = System(self.world)

        for thing in ['string', [], {}, foo]:
            with self.assertRaises(TypeError):
                self.world.subscribe(some_kind_of_system, 'do_something', thing, after=True)

    def test_must_choose_a_time_for_callback_to_be_called(self):
        def callback_method(*args):
            pass

        some_kind_of_system = System(self.world)

        with self.assertRaises(ValueError):
            self.world.subscribe(some_kind_of_system, 'do_something', callback_method)
