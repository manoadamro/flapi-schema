import functools
from typing import Any, Callable, Type, Union

import flask

from . import errors, types


class Body(dict):
    def __init__(self, body):
        body = body or {}
        super(Body, self).__init__(**body)

    def __getattr__(self, item):
        try:
            return self[item]
        except KeyError as ex:
            raise AttributeError(ex)

    def __setattr__(self, key, value):
        try:
            self[key] = value
        except KeyError as ex:
            raise AttributeError(ex)


class Protect:
    def __init__(
        self,
        rule: Union[
            bool,
            Type[types.Schema],
            types.Schema,
            Type[types.Property],
            types.Property,
            Type[types.Rule],
            types.Rule,
            None,
        ],
    ):
        self.rule = (
            rule()
            if isinstance(rule, type)
            and issubclass(rule, (types.Property, types.Schema))
            else rule
        )

    @property
    def request_body(self):
        if self.rule is True:
            if not flask.request.is_json:
                raise errors.SchemaValidationError(
                    "request was expected to contain json"
                )
            return flask.request.json
        if self.rule is False:
            if flask.request.is_json:
                raise errors.SchemaValidationError(
                    "request was not expected to contain json"
                )
            return None
        if self.rule is None:
            if flask.request.is_json:
                return flask.request.json
            return None
        if isinstance(self.rule, (types.Property, types.Schema)):
            return self.rule(flask.request.json)
        raise errors.SchemaValidationError(f"unknown rule {self.rule}")

    def __call__(self, func: Callable) -> Callable:
        @functools.wraps(func)
        def _call(*args: Any, **kwargs: Any) -> Any:
            body = Body(self.request_body) or None
            return func(body, *args, **kwargs)

        return _call
