import unittest

import flapi_schema.errors
import flapi_schema.types


class BasicSchema(flapi_schema.types.Schema):
    thing = flapi_schema.types.Bool()


class ObjectTest(unittest.TestCase):
    def test_strict(self):
        prop = flapi_schema.types.Object(BasicSchema, strict=True)
        self.assertRaises(
            flapi_schema.errors.SchemaValidationError,
            prop,
            {"thing": False, "other": 12},
        )

    def test_nullable_by_default(self):
        prop = flapi_schema.types.Object(BasicSchema)
        self.assertIsNone(prop(None))

    def test_nullable_allows_null(self):
        prop = flapi_schema.types.Object(BasicSchema, nullable=True)
        self.assertIsNone(prop(None))

    def test_nullable_raises_error(self):
        prop = flapi_schema.types.Object(BasicSchema, nullable=False)
        self.assertRaises(flapi_schema.errors.SchemaValidationError, prop, None)

    def test_wrong_type(self):
        prop = flapi_schema.types.Object(BasicSchema, callback=None)
        self.assertRaises(flapi_schema.errors.SchemaValidationError, prop, 12)

    def test_callback(self):
        prop = flapi_schema.types.Object(
            BasicSchema, callback=lambda v: {"thing": True}
        )
        self.assertEqual(prop({"thing": False}), {"thing": True})

    def test_no_callback(self):
        prop = flapi_schema.types.Object(BasicSchema, callback=None)
        self.assertEqual(prop({"thing": False}), {"thing": False})
