import unittest

from flapi_schema.types import NoneOf


class NoneOfTest(unittest.TestCase):
    def test_any_of(self):
        rule = NoneOf(lambda _: False, lambda _: False)
        self.assertTrue(rule({}))

    def test_fails(self):
        rule = NoneOf(lambda _: False, lambda _: True)
        self.assertFalse(rule({}))
