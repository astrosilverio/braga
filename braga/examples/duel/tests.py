import unittest
from mock import patch

import six

from braga import Assemblage, World, Manager
from braga.examples import duel


def get_exception_message(exception):
    exception_message = ''
    if six.PY2:
        exception_message = exception.message
    if six.PY3:
        exception_message = str(exception)
    return exception_message


class TestEquipmentSystem(unittest.TestCase):

    def setUp(self):
        self.world = World()
        self.player = self.world.make_entity(Assemblage([duel.EquipmentBearing]))

        self.wand_factory = Assemblage([duel.Equipment], equipment_type='wand')
        self.wand = self.world.make_entity(self.wand_factory)

    def test_player_has_no_equipment(self):
        self.assertFalse(hasattr(self.player, 'wand'))

    def test_nonbearer_item_cannot_equip_equipment(self):
        second_wand = self.world.make_entity(self.wand_factory)

        with self.assertRaises(ValueError) as e:
            duel.equipment_system.equip(self.wand, second_wand)

        self.assertEqual(get_exception_message(e.exception), "That cannot equip other items")

    def test_player_equips_an_item(self):
        duel.equipment_system.equip(self.player, self.wand)

        self.assertEqual(self.player.wand, self.wand)

    def test_player_cannot_equip_two_items(self):
        """ In other minigames, you will be allowed to equip an arbitrary number
            of items, but that is not necessary for the duel simulator.
        """
        duel.equipment_system.equip(self.player, self.wand)

        second_wand = self.world.make_entity(self.wand_factory)

        with self.assertRaises(ValueError) as e:
            duel.equipment_system.equip(self.player, second_wand)

        self.assertEqual(get_exception_message(e.exception), "You are already equipping an item of this type")

        self.assertEqual(self.player.wand, self.wand)

    def test_unequipping_an_item(self):
        duel.equipment_system.equip(self.player, self.wand)
        duel.equipment_system.unequip(self.player, self.wand)

        self.assertFalse(hasattr(self.player, 'wand'))

    def test_unequipping_and_reequipping_an_item(self):
        duel.equipment_system.equip(self.player, self.wand)
        duel.equipment_system.unequip(self.player, self.wand)

        second_wand = self.world.make_entity(self.wand_factory)
        duel.equipment_system.equip(self.player, second_wand)

        self.assertEqual(self.player.wand, second_wand)


class TestContainerSystem(unittest.TestCase):

    def setUp(self):
        self.world = World()
        bucket_factory = Assemblage(components=[duel.Container])
        self.bucket_one = self.world.make_entity(bucket_factory)
        self.bucket_two = self.world.make_entity(bucket_factory)

        self.thing_factory = Assemblage(components=[duel.Moveable])
        self.thing = self.world.make_entity(self.thing_factory, location=self.bucket_one)
        self.bucket_one.inventory.add(self.thing)

    def test_move_item_to_new_inventory(self):
        duel.container_system.move(self.thing, self.bucket_two)

        self.assertEqual(self.thing.location, self.bucket_two)
        self.assertEqual(self.bucket_two.inventory, set([self.thing]))

    def test_cannot_move_immoveable_item(self):
        bookcase = self.world.make_entity()

        with self.assertRaises(ValueError) as e:
            duel.container_system.move(bookcase, self.bucket_two)

        self.assertEqual(get_exception_message(e.exception), "You cannot move this item")
        self.assertEqual(self.bucket_two.inventory, set([]))

    def test_cannot_move_item_to_non_container(self):
        new_thing = self.thing_factory.make()
        with self.assertRaises(ValueError) as e:
            duel.container_system.move(self.thing, new_thing)

        self.assertEqual(get_exception_message(e.exception), "Invalid destination")
        self.assertEqual(self.thing.location, self.bucket_one)


class TestLexing(unittest.TestCase):

    def setUp(self):
        self.name_manager = Manager(duel.Name)

    def test_get_entity_from_name_returns_appropriate_entity(self):
        toothbrush = Assemblage(components=[duel.Name]).make(name='toothbrush')
        self.name_manager.register(toothbrush)
        expected_token = ('entity', toothbrush)

        with patch.object(duel.duel, 'name_manager', self.name_manager):
            lexed_value = duel.name_system.lex("toothbrush")

        self.assertEqual(expected_token, lexed_value)

    def test_get_entity_from_name_assumes_literal_if_entity_does_not_exist(self):
        toothbrush = Assemblage(components=[duel.Name]).make(name='toothbrush')
        self.name_manager.register(toothbrush)
        expected_token = ('literal', "razor")

        with patch.object(duel.duel, 'name_manager', self.name_manager):
            lexed_value = duel.name_system.lex("razor")

        self.assertEqual(expected_token, lexed_value)

    def test_get_entity_from_multiword_token_returns_appropriate_entity(self):
        toothpaste = Assemblage(components=[duel.Name]).make(name='toothpaste')
        self.name_manager.register(toothpaste)
        expected_token = ('entity', toothpaste)

        with patch.object(duel.duel, 'name_manager', self.name_manager):
            lexed_value = duel.name_system.lex("tube of toothpaste")

        self.assertEqual(expected_token, lexed_value)

    def test_get_token_for_verb_returns_appropriate_verb(self):
        expected_token = ('verb', 'command_for_put_goes_here')
        lexed_value = duel.name_system.lex('put')
        self.assertEqual(expected_token, lexed_value)


class TestTokenizing(unittest.TestCase):

    def setUp(self):
        self.name_manager = Manager(duel.Name)

    def test_tokenizing_input_string_breaks_string_into_words(self):
        tokenized_input = duel.name_system.tokenize("razor toothbrush")
        self.assertEqual(tokenized_input, ["razor", "toothbrush"])

    def test_tokenizing_input_string_catches_multiword_tokens(self):
        tokenized_input = duel.name_system.tokenize("tube of toothpaste and floss")
        self.assertEqual(tokenized_input, ["tube of toothpaste", "floss"])


class TestParsing(unittest.TestCase):

    def setUp(self):
        self.name_manager = Manager(duel.Name)

    def test_parsing_token_list_generates_appropriate_tree(self):
        toothpaste = Assemblage(components=[duel.Name]).make(name='toothpaste')
        toothbrush = Assemblage(components=[duel.Name]).make(name='toothbrush')
        self.name_manager.register(toothpaste)
        self.name_manager.register(toothbrush)

        with patch.object(duel.duel, 'name_manager', self.name_manager):
            parsed_input = duel.name_system.parse([('verb', 'command_for_put_goes_here'), ('entity', toothpaste), ('entity', toothbrush)])

        self.assertEqual(parsed_input, ('command_for_put_goes_here', (toothpaste, toothbrush)))

    def test_literals_can_be_ignored_in_appropriate_places(self):
        with patch.object(duel.duel, 'name_manager', self.name_manager):
            parsed_input = duel.name_system.parse([('literal', 'print'), ('verb', 'command_for_inventory_goes_here')])

        self.assertEqual(parsed_input, ('command_for_inventory_goes_here', ()))
