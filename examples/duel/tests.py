import unittest

from braga import Entity, Assemblage
from examples.duel import duel


class TestEquipmentSystemBase(unittest.TestCase):

    def setUp(self):
        self.player = Entity()

        self.small_equipment_factory = Assemblage(components=[duel.Equipment])
        self.wand = self.small_equipment_factory.make(equipment_type='wand')
        self.quill = self.small_equipment_factory.make(equipment_type='quill')

        self.equipment_system = duel.EquipmentSystem()


class TestEquippingItems(TestEquipmentSystemBase):

    def test_player_equips_first_item(self):
        self.equipment_system.equip(self.player, self.wand, True)

        self.assertEqual(self.player.wand, self.wand)
        self.assertEqual(self.player.equipment, [self.wand])

    def test_player_can_equip_two_items(self):
        self.equipment_system.equip(self.player, self.wand)
        self.equipment_system.equip(self.player, self.quill, True)

        self.assertItemsEqual(self.player.equipment, [self.wand, self.quill])
        self.assertEqual(self.player.wand, self.wand)
        self.assertEqual(self.player.quill, self.quill)

    def test_equipping_another_instance_of_same_equipment_type(self):
        """ I am mostly just curious about how this will work."""
        self.equipment_system.equip(self.player, self.quill)

        second_quill = self.small_equipment_factory.make(equipment_type='quill')
        self.equipment_system.equip(self.player, second_quill, True)

        self.assertItemsEqual(self.player.equipment, [self.quill, second_quill])
        self.assertEqual(self.player.quill, second_quill)

    def test_player_cannot_equip_three_items(self):
        self.equipment_system.equip(self.player, self.wand)
        self.equipment_system.equip(self.player, self.quill)

        fork = self.small_equipment_factory.make(equipment_type='fork')

        with self.assertRaises(ValueError) as e:
            self.equipment_system.equip(self.player, fork)

        self.assertEqual(e.exception.message, "You cannot equip that at this time")


class TestUnequippingItems(TestEquipmentSystemBase):

    def setUp(self):
        super(TestUnequippingItems, self).setUp()
        self.equipment_system.equip(self.player, self.wand, True)

    def test_unequipping_one_item(self):
        self.equipment_system.unequip(self.player, self.wand, True)

        self.assertEqual(self.player.equipment, [])
        self.assertFalse(hasattr(self.player, 'wand'))

    def test_unequipping_more_recent_instance_of_same_equipment_type(self):
        second_wand = self.small_equipment_factory.make(equipment_type='wand')
        self.equipment_system.equip(self.player, second_wand, True)

        self.equipment_system.unequip(self.player, second_wand, True)

        self.assertEqual(self.player.equipment, [self.wand])
        self.assertEqual(self.player.wand, self.wand)

    def test_unequipping_older_instance_of_same_equipment_type(self):
        second_wand = self.small_equipment_factory.make(equipment_type='wand')
        self.equipment_system.equip(self.player, second_wand, True)

        self.equipment_system.unequip(self.player, self.wand, True)

        self.assertEqual(self.player.equipment, [second_wand])
        self.assertEqual(self.player.wand, second_wand)
