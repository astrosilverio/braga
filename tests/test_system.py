import unittest
from mock import patch

from braga import System, World


def before_child_method_runs(arg_one, kwarg_two=False):
    pass


def after_child_method_runs(arg_one, kwarg_two=False):
    pass


class TestSystem(unittest.TestCase):

    def test_child_methods_are_decorated(self):
        world = World()
        system = System(world)

        @system
        def child_method(arg_one, kwarg_two=False):
            pass

        self.assertIn('run_hooks', system.child_method.func_code.co_names)

    @patch('tests.test_system.before_child_method_runs')
    def test_child_methods_look_for_before_hooks(self, callback_mock):
        world = World()
        system = System(world)

        @system
        def child_method(arg_one, kwarg_two=False):
            pass

        world.subscribe(system, 'child_method', before_child_method_runs, before=True)

        system.child_method('first_arg', kwarg_two='keyword_arg')

        callback_mock.assert_called_once_with('first_arg', kwarg_two='keyword_arg')

    @patch('tests.test_system.after_child_method_runs')
    def test_child_methods_look_for_after_hooks(self, callback_mock):
        world = World()
        system = System(world)

        @system
        def child_method(arg_one, kwarg_two=False):
            pass

        world.subscribe(system, 'child_method', after_child_method_runs, after=True)

        system.child_method('first_arg', kwarg_two='keyword_arg')

        callback_mock.assert_called_once_with('first_arg', kwarg_two='keyword_arg')
