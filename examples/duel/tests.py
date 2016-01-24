import unittest

from braga import Entity, Assemblage
from examples.duel import duel


class TestEquipmentSystem(unittest.TestCase):

    def setUp(self):
        self.player = Entity()

        self.wand_factory = Assemblage(components={duel.Equipment: {'equipment_type': 'wand'}})
        self.wand = self.wand_factory.make()

        self.equipment_system = duel.EquipmentSystem()

    def test_player_has_no_equipment(self):
        self.assertFalse(hasattr(self.player, 'wand'))

    def test_player_equips_an_item(self):
        self.equipment_system.equip(self.player, self.wand)

        self.assertEqual(self.player.wand, self.wand)

    def test_player_cannot_equip_two_items(self):
        """ In other minigames, you will be allowed to equip an arbitrary number
            of items, but that is not necessary for the duel simulator.
        """
        self.equipment_system.equip(self.player, self.wand)

        second_wand = self.wand_factory.make()

        with self.assertRaises(ValueError) as e:
            self.equipment_system.equip(self.player, second_wand)

        self.assertEqual(e.exception.message, "You cannot equip that at this time")

        self.assertEqual(self.player.wand, self.wand)

    def test_unequipping_an_item(self):
        self.equipment_system.equip(self.player, self.wand)
        self.equipment_system.unequip(self.player, self.wand)

        self.assertFalse(hasattr(self.player, 'wand'))

    def test_unequipping_and_reequipping_an_item(self):
        self.equipment_system.equip(self.player, self.wand)
        self.equipment_system.unequip(self.player, self.wand)

        second_wand = self.wand_factory.make()
        self.equipment_system.equip(self.player, second_wand)

        self.assertEqual(self.player.wand, second_wand)
