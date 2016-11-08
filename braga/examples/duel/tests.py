import unittest

from braga import Assemblage, World
from braga.examples import duel


class TestEquipmentSystem(unittest.TestCase):

    def setUp(self):
        self.world = World()
        self.player = self.world.make_entity(Assemblage([duel.EquipmentBearing]))

        self.wand_factory = Assemblage([duel.Equipment], equipment_type='wand')
        self.wand = self.world.make_entity(self.wand_factory)

        self.equipment_system = duel.EquipmentSystem(world=self.world, auto_update=True)

    def test_player_has_no_equipment(self):
        self.assertFalse(hasattr(self.player, 'wand'))

    def test_nonbearer_item_cannot_equip_equipment(self):
        second_wand = self.world.make_entity(self.wand_factory)

        with self.assertRaises(ValueError) as e:
            self.equipment_system.equip(self.wand, second_wand)

        self.assertEqual(e.exception.message, "That cannot equip other items")

    def test_player_equips_an_item(self):
        self.equipment_system.equip(self.player, self.wand)

        self.assertEqual(self.player.wand, self.wand)

    def test_player_cannot_equip_two_items(self):
        """ In other minigames, you will be allowed to equip an arbitrary number
            of items, but that is not necessary for the duel simulator.
        """
        self.equipment_system.equip(self.player, self.wand)

        second_wand = self.world.make_entity(self.wand_factory)

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

        second_wand = self.world.make_entity(self.wand_factory)
        self.equipment_system.equip(self.player, second_wand)

        self.assertEqual(self.player.wand, second_wand)


class TestContainerSystem(unittest.TestCase):

    def setUp(self):
        self.world = World()
        bucket_factory = Assemblage(components=[duel.Container])
        self.bucket_one = self.world.make_entity(bucket_factory)
        self.bucket_two = self.world.make_entity(bucket_factory)

        self.thing_factory = Assemblage(components=[duel.Moveable])
        self.thing = self.world.make_entity(self.thing_factory, location=self.bucket_one)

        self.container_system = duel.ContainerSystem(world=self.world, auto_update=True)

    def test_move_item_to_new_inventory(self):
        self.container_system.move(self.thing, self.bucket_two)

        self.assertEqual(self.thing.location, self.bucket_two)
        self.assertEqual(self.bucket_two.inventory, set([self.thing]))

    def test_cannot_move_immoveable_item(self):
        bookcase = self.world.make_entity()

        with self.assertRaises(ValueError) as e:
            self.container_system.move(bookcase, self.bucket_two)

        self.assertEqual(e.exception.message, "You cannot move this item")
        self.assertEqual(self.bucket_two.inventory, set([]))

    def test_cannot_move_item_to_non_container(self):
        new_thing = self.thing_factory.make()
        with self.assertRaises(ValueError) as e:
            self.container_system.move(self.thing, new_thing)

        self.assertEqual(e.exception.message, "Invalid destination")
        self.assertEqual(self.thing.location, self.bucket_one)


class TestNameSystem(unittest.TestCase):

    def setUp(self):
        self.world = World()
        self.item_factory = Assemblage(components=[duel.Name])
        self.item = self.world.make_entity(self.item_factory, name='item one')

        self.name_system = duel.NameSystem(world=self.world)

    def test_entity_retrievable_from_name(self):
        entity = self.name_system.get_entity_from_name('item one')
        self.assertEqual(entity, self.item)

    def test_none_returned_for_unknown_name(self):
        self.assertIsNone(self.name_system.get_entity_from_name('asdfdsa'))

    def test_aliases_can_be_created(self):
        self.name_system.add_alias('cool item', self.item)

        self.assertIn('cool item', self.name_system.names.keys())
        self.assertEqual(self.name_system.names['cool item'], self.item)

    def test_no_dupliate_names_can_be_added(self):
        with self.assertRaises(ValueError) as e:
            self.name_system.add_alias('item one', self.item)

        self.assertEqual(e.exception.message, 'Duplicate entity names')

    def test_names_in_tokens_property(self):
        self.assertEqual(self.name_system.tokens, self.name_system.names.keys())


class TestDescriptionSystem(unittest.TestCase):

    def setUp(self):
        self.world = World()
        self.world.add_system(duel.NameSystem)
        self.description_system = self.world.add_system(duel.DescriptionSystem)

    def test_chained_reference_resolves_correctly(self):
        player = self.world.make_entity(
            duel.player_factory,
            name='Hermione Granger',
            description="Is she as good at duelling as she is at transfiguration? Hermione's skill level is ${self.skill}.",
            skill=15)
        self.world.refresh()

        self.assertEqual(
            self.description_system.populate_description(player),
            "Is she as good at duelling as she is at transfiguration? Hermione's skill level is 15.")
