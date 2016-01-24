import unittest

from braga import Entity, Assemblage
from examples.duel import duel


class TestEquipmentSystem(unittest.TestCase):

    def setUp(self):
        self.player = Entity()

        self.small_equipment_factory = Assemblage(components=[duel.Equipment])
        self.wand = self.small_equipment_factory.make(equipment_type='wand')
        self.quill = self.small_equipment_factory.make(equipment_type='quill')

        self.equipment_system = duel.EquipmentSystem()

    def test_player_equips_first_item(self):
        self.equipment_system.equip(self.player, self.wand)

        self.assertEqual(self.player.wand, self.wand)
        self.assertEqual(self.player.equipment, [self.wand])

    def test_player_can_equip_two_items(self):
        self.equipment_system.equip(self.player, self.wand)
        self.equipment_system.equip(self.player, self.quill)

        self.assertEqual(self.player.wand, self.wand)
        self.assertEqual(self.player.quill, self.quill)
        self.assertItemsEqual(self.player.equipment, [self.wand, self.quill])

    def test_equipping_another_instance_of_same_equipment_type(self):
        """ Double equipping will be allowed for other games but not the duel,
            as I do not think it makes sense for a player to simultaneously
            equip two wands, and wands are the only equippable items in this game.
        """
        self.equipment_system.equip(self.player, self.quill)

        second_quill = self.small_equipment_factory.make(equipment_type='quill')

        with self.assertRaises(ValueError) as e:
            self.equipment_system.equip(self.player, second_quill)

        self.assertEqual(e.exception.message, "You cannot equip that at this time")

        self.assertEqual(self.player.quill, self.quill)
        self.assertItemsEqual(self.player.equipment, [self.quill])

    def test_player_cannot_equip_three_items(self):
        self.equipment_system.equip(self.player, self.wand)
        self.equipment_system.equip(self.player, self.quill)

        fork = self.small_equipment_factory.make(equipment_type='fork')

        with self.assertRaises(ValueError) as e:
            self.equipment_system.equip(self.player, fork)

        self.assertEqual(e.exception.message, "You cannot equip that at this time")
        self.assertItemsEqual(self.player.equipment, [self.wand, self.quill])

    def test_unequipping_an_item(self):
        self.equipment_system.equip(self.player, self.wand)
        self.equipment_system.unequip(self.player, self.wand)

        self.assertEqual(self.player.equipment, [])
        self.assertFalse(hasattr(self.player, 'wand'))
