import unittest

import flapi_schema.errors
import flapi_schema.types


class NumberTest(unittest.TestCase):

    # NUMBER TESTS

    def test_min_only(self):
        prop = flapi_schema.types.Number(min_value=0)
        self.assertEqual(prop(5), 5)

    def test_min_only_out_of_range(self):
        prop = flapi_schema.types.Number(min_value=0)
        self.assertRaises(flapi_schema.errors.SchemaValidationError, prop, -1)

    def test_max_only(self):
        prop = flapi_schema.types.Number(max_value=10)
        self.assertEqual(prop(5), 5)

    def test_max_only_out_of_range(self):
        prop = flapi_schema.types.Number(max_value=10)
        self.assertRaises(flapi_schema.errors.SchemaValidationError, prop, 20)

    def test_min_and_max(self):
        prop = flapi_schema.types.Number(min_value=0, max_value=10)
        self.assertEqual(prop(5), 5)

    def test_min_and_max_out_of_range(self):
        prop = flapi_schema.types.Number(min_value=0, max_value=10)
        self.assertRaises(flapi_schema.errors.SchemaValidationError, prop, 20)

    def test_no_range(self):
        prop = flapi_schema.types.Number()
        self.assertEqual(prop(20), 20)

    # PROPERTY TESTS

    def test_nullable_by_default(self):
        prop = flapi_schema.types.Number()
        self.assertIsNone(prop(None))

    def test_nullable_allows_null(self):
        prop = flapi_schema.types.Number(nullable=True)
        self.assertIsNone(prop(None))

    def test_nullable_raises_error(self):
        prop = flapi_schema.types.Number(nullable=False)
        self.assertRaises(flapi_schema.errors.SchemaValidationError, prop, None)

    def test_default_is_none(self):
        prop = flapi_schema.types.Number(default=None)
        self.assertIsNone(prop(None))

    def test_default_value(self):
        prop = flapi_schema.types.Number(default=12)
        self.assertEqual(prop(None), 12)

    def test_default_passive_when_value_not_none(self):
        prop = flapi_schema.types.Number(default=12)
        self.assertEqual(prop(21), 21)

    def test_default_callable(self):
        prop = flapi_schema.types.Number(default=lambda: 12)
        self.assertEqual(prop(None), 12)

    def test_wrong_type(self):
        prop = flapi_schema.types.Number(callback=None)
        self.assertRaises(flapi_schema.errors.SchemaValidationError, prop, "nope")

    def test_callback(self):
        prop = flapi_schema.types.Number(callback=lambda v: v * 2)
        self.assertEqual(prop(12), 24)

    def test_no_callback(self):
        prop = flapi_schema.types.Number(callback=None)
        self.assertEqual(prop(12), 12)
