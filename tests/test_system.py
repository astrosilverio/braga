import unittest

from braga.models import System


class BadSystem(System):
    pass


class GoodSystem(System):

    def __init__(self):
        super(GoodSystem, self).__init__()

    def update(self):
        pass


class TestSystem(unittest.TestCase):

    def test_must_implement_update_method(self):
        with self.assertRaises(TypeError):
            BadSystem()

    def test_has_thread(self):
        good = GoodSystem()
        self.assertFalse(good.thread)
        good.start()
        self.assertTrue(good.thread)
