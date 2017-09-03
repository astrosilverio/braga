import unittest

from braga import Assemblage, World
from braga.examples import duel


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

        self.assertEqual(e.exception.message, "That cannot equip other items")

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

        self.assertEqual(e.exception.message, "You are already equipping an item of this type")

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

        self.assertEqual(e.exception.message, "You cannot move this item")
        self.assertEqual(self.bucket_two.inventory, set([]))

    def test_cannot_move_item_to_non_container(self):
        new_thing = self.thing_factory.make()
        with self.assertRaises(ValueError) as e:
            duel.container_system.move(self.thing, new_thing)

        self.assertEqual(e.exception.message, "Invalid destination")
        self.assertEqual(self.thing.location, self.bucket_one)
