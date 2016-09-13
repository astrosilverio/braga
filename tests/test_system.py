import unittest
from mock import Mock, patch

from braga import System, World


class BadSystem(System):
    def __init__(self):
        super(BadSystem, self).__init__(world=Mock())


class GoodSystem(System):

    def __init__(self, world):
        super(GoodSystem, self).__init__(world=world)

    def child_method(self, arg_one, kwarg_two=False):
        pass

    def update(self):
        pass


def before_child_method_runs(system, arg_one, kwarg_two=False):
    pass


def after_child_method_runs(system, arg_one, kwarg_two=False):
    pass


class TestSystem(unittest.TestCase):

    def test_must_implement_update_method(self):
        with self.assertRaises(TypeError):
            BadSystem()

    # def test_has_thread(self):
    #     good = GoodSystem('world')
    #     self.assertFalse(good.thread)
    #     good.start()
    #     self.assertTrue(good.thread)

    def test_child_methods_are_decorated(self):
        world = World()
        system = GoodSystem(world)
        self.assertIn('run_hooks', system.child_method.__func__.func_code.co_names)

    @patch('tests.test_system.before_child_method_runs')
    def test_child_methods_look_for_before_hooks(self, callback_mock):
        world = World()
        system = GoodSystem(world)
        world.subscribe(system, 'child_method', before_child_method_runs, before=True)

        system.child_method('first_arg', kwarg_two='keyword_arg')

        callback_mock.assert_called_once_with(system, 'first_arg', kwarg_two='keyword_arg')
