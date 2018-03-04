import unittest
from collections import defaultdict

import six

from braga import Component, Manager, Assemblage


class ComponentWithState(Component):

    INITIAL_PROPERTIES = ['number', 'letter']

    def __init__(self, number=None, letter=None):
        self.number = number
        self.letter = letter


class TestManager(unittest.TestCase):

    def test_properties_default_to_initial_properties(self):
        manager = Manager(ComponentWithState)
        self.assertEqual(manager.properties_to_register, ['number', 'letter'])

    def test_registry_names_built_correctly_with_initial_properties(self):
        manager = Manager(ComponentWithState)
        self.assertIn('entities_by_number', six.iterkeys(manager.__dict__))
        self.assertIn('entities_by_letter', six.iterkeys(manager.__dict__))

    def test_registry_names_built_correctly_with_defined_properties(self):
        manager = Manager(ComponentWithState, properties_to_register=['location'])
        self.assertIn('entities_by_location', six.iterkeys(manager.__dict__))
        self.assertNotIn('entities_by_number', six.iterkeys(manager.__dict__))
        self.assertNotIn('entities_by_letter', six.iterkeys(manager.__dict__))

    def test_registries_are_default_dicts(self):
        manager = Manager(ComponentWithState)
        self.assertEqual(manager.entities_by_number, defaultdict(list))
        self.assertEqual(manager.entities_by_letter, defaultdict(list))

    def test_register_puts_entity_in_appropriate_registry(self):
        manager = Manager(ComponentWithState)
        entity = Assemblage(components=[ComponentWithState]).make(number=1, letter='a')

        manager.register(entity)

        self.assertIn(1, six.iterkeys(manager.entities_by_number))
        self.assertIn(entity, manager.entities_by_number[1])
        self.assertIn('a', six.iterkeys(manager.entities_by_letter))
        self.assertIn(entity, manager.entities_by_letter['a'])

    def test_register_stores_entity_by_component(self):
        manager = Manager(ComponentWithState)
        entity = Assemblage(components=[ComponentWithState]).make(number=1, letter='b')
        specific_component = entity.get_component(ComponentWithState)

        manager.register(entity)

        self.assertEqual(manager.entities_by_component[specific_component], entity)
