import unittest
import unittest.mock

import flask

import flapi_schema.errors
import flapi_schema.protect
import flapi_schema.types


class FakeSchema(flapi_schema.types.Schema):
    __strict__ = True
    test = flapi_schema.types.Bool()


def route(json_body):
    return json_body


class SchemaProtectTest(unittest.TestCase):
    def setUp(self):
        self.app = flask.Flask("TestFlask")

    @unittest.mock.patch.object(
        flask, "request", unittest.mock.Mock(json={"test": True})
    )
    def test_expects_specific_json(self):
        func = flapi_schema.protect(FakeSchema)(route)
        self.assertEqual(func(), {"test": True})

    @unittest.mock.patch.object(
        flask, "request", unittest.mock.Mock(json={"nope": True})
    )
    def test_fails_when_expecting_specific_json(self):
        func = flapi_schema.protect(FakeSchema)(route)
        self.assertRaises(flapi_schema.errors.SchemaValidationError, func)

    @unittest.mock.patch.object(
        flask, "request", unittest.mock.Mock(json={"anything": 123})
    )
    def test_expects_any_json(self):
        func = flapi_schema.protect(True)(route)
        self.assertEqual(func(), {"anything": 123})

    @unittest.mock.patch.object(flask, "request", unittest.mock.Mock(is_json=False))
    def test_fails_when_expecting_any_json(self):
        func = flapi_schema.protect(True)(route)
        self.assertRaises(flapi_schema.errors.SchemaValidationError, func)

    @unittest.mock.patch.object(flask, "request", unittest.mock.Mock(is_json=False))
    def test_expects_no_json(self):
        func = flapi_schema.protect(False)(route)
        self.assertEqual(func(), None)

    @unittest.mock.patch.object(flask, "request", unittest.mock.Mock(is_json=True))
    def test_fails_when_expecting_no_json(self):
        func = flapi_schema.protect(False)(route)
        self.assertRaises(flapi_schema.errors.SchemaValidationError, func)

    @unittest.mock.patch.object(flask, "request", unittest.mock.Mock(is_json=False))
    def test_expects_any_or_no_json_gets_none(self):
        func = flapi_schema.protect(None)(route)
        self.assertEqual(func(), None)

    @unittest.mock.patch.object(
        flask, "request", unittest.mock.Mock(is_json=True, json={"yep": 123})
    )
    def test_expects_any_or_no_json_gets_json(self):
        func = flapi_schema.protect(None)(route)
        self.assertEqual(func(), {"yep": 123})

    @unittest.mock.patch.object(flask, "request", unittest.mock.Mock())
    def test_wrong_type(self):
        func = flapi_schema.protect(123)(route)
        self.assertRaises(flapi_schema.errors.SchemaValidationError, func)
