[![CircleCI](https://circleci.com/gh/manoadamro/flapi/tree/master.svg?style=svg)](https://circleci.com/gh/manoadamro/flapi-schema/tree/master)
[![Coverage Status](https://coveralls.io/repos/github/manoadamro/flapi/badge.svg?branch=master)](https://coveralls.io/github/manoadamro/flapi-schema?branch=master)
[![CodeFactor](https://www.codefactor.io/repository/github/manoadamro/flapi/badge)](https://www.codefactor.io/repository/github/manoadamro/flapi-schema)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

---

# flapi-schema

```python

def get_minimum_dob():
    return (datetime.datetime.utcnow() - datetime.timedelta(days=365.25 * 16)).date()


class Address(Schema):
    number = Int(min_value=0, nullable=False)
    post_code = Regex(
        re.compile("[a-zA-z]{2}[0-9] ?[0-9][a-zA-z]{2}"), nullable=False
    )


class Items(Schema):
    name = String(min_length=3, max_length=50, nullable=False)
    count = Int(min_value=0, default=0)


class Person(Schema):
    __strict__ = True
    name = String(min_length=3, max_length=50, nullable=False)
    address = Object(Address, nullable=False, strict=True)
    friends = Array(Uuid, default=[])
    items = Array(Object(Items, strict=False), default=[])
    date_of_birth = Date(max_value=get_minimum_dob, nullable=False)
    date_of_death = Date(max_value=datetime.date.today, nullable=True)

    @custom_property(int, float, nullable=False)
    def something(cls, value):
        return value * 2
```

## Schema(...)

Base class for schema definitions

```python

class MySchema(Schema):
    ...

```

Notes:

- Anything (including methods) defined in schema classes will be considered a property.
 If you wish to hide an attribute/method you will need to prefix it with an underscore

- You can define properties using a method without the `@custom_property` decorator.
 This will mean you are passed value with no checks having been done on it.

- To mark a schema as "strict" (meaning extra keys are not accepted),
 add `__strict__ = True` as an attribute

## protect(...)

```python
@protect(MySchema)
def some_method():
    ...
```

__schema__: Schema, Property or Rule (required) The check that has to pass in order for the decorated method to be called. see [flapi_schema.types](#Schema-Types)

---

# Schema Types

## Property(...)

Base class for all JWT rules.
<br>
Can be used to build custom property

```python
class MyProperty:
    def __init__(self, multiplier, **kwargs):
        # call super and tell Property we only accept ints or floats,
        # pass on any kwargs
        super(DateTime, self).__init__(int, float, **kwargs)
        self.multiplier = multiplier

    def __call__(self, item):
        # do the default checks by calling super(),
        # get back an updated value
        value = super(Array, self).__call__(value)

        # do the property thing
        return value * multiplier

```

__types__: tuple of types (required) Accepted value types

__nullable__: bool (default True) If false, an error will be raised if a null value is receeved

__default__: Any (default None) If a null value is a received, it will be replaced with this

__callback__: Callable (default None) A method to call once all checks are complete.
This method receives the value as its only parameter and returns a modified value

## custom_property(...)

Does the same as [Property](#Property) but as a decorator!

```python
@custom_property(int, float, nullable=False)
def something(cls, value):
    return value * 2

@custom_property(int, float, default=1)
def something_else(cls, value):
    return value * 3
```

__types__: tuple of types (required) Accepted value types

__nullable__: bool (default True) If false, an error will be raised if a null value is receeved

__default__: Any (default None) If a null value is a received, it will be replaced with this

__callback__: Callable (default None) A method to call once all checks are complete.
This method receives the value as its only parameter and returns a modified value

## Object(...)

Allows nesting of schemas

```python
class Address(Schema):
    number = Int(min_value=0, nullable=False)
    post_code = Regex(
        re.compile("[a-zA-z]{2}[0-9] ?[0-9][a-zA-z]{2}"), nullable=False
    )

class Person(Schema):
    address = Object(Address, nullable=False, strict=True)
```

__strict__: bool (default False) overrides `__strict__` attribute on schema definition

__nullable__: bool (default True) If false, an error will be raised if a null value is receeved

__default__: Any (default None) If a null value is a received, it will be replaced with this

__callback__: Callable (default None) A method to call once all checks are complete.
This method receives the value as its only parameter and returns a modified value

## Array(...)

Defines an array of items conforming to a Schema/Property definition

```python
class MySchema(Schema):
    items = Array(Object(Item, strict=False), default=[])
```

__min_length__: Property or Rule (required)

__min_length__: int or callable returning int (default None) Minimum allowed array length

__max_length__: int or callable returning int (default None) Maximum allowed array length

__callback__: Callable (default None) A method to call once all checks are complete.
This method receives the value as its only parameter and returns a modified value

Notes:

- Value will default to an empty array if none

## Choice(...)

Ensures a value is equal to one from a defined set.

```python
class MySchema(Schema):
    choice = Choice([Bool(), Int(), "1", "2"], nullable=False)
```

__choices__: list (required) A list containing specific valid values, Property definitions or a mix of the two.

__nullable__: bool (default True) If false, an error will be raised if a null value is receeved

__default__: Any (default None) If a null value is a received, it will be replaced with this

__callback__: Callable (default None) A method to call once all checks are complete.
This method receives the value as its only parameter and returns a modified value

Notes:

- If a value conforms to more than one choice, it will be validated against the first valid one.

## Number(...)

Ensures a value is either an in or a float

```python
class MySchema(Schema):
    number = Number(min_value=0, max_value=10, nullable=False, default=2)
```

__min_value__: int, float or callable returning int or float (default None) Minimum allowed value

__max_value__: int, float or callable returning int or float (default None) Maximum allowed value

__nullable__: bool (default True) If false, an error will be raised if a null value is receeved

__default__: Any (default None) If a null value is a received, it will be replaced with this

__callback__: Callable (default None) A method to call once all checks are complete.
This method receives the value as its only parameter and returns a modified value

## Int(...)

Ensures a value is an integer

```python
class MySchema(Schema):
    number = Int(min_value=0, max_value=10, nullable=False, default=2)
```

__min_value__: int or callable returning int (default None) Minimum allowed value

__max_value__: int or callable returning int (default None) Maximum allowed value

__nullable__: bool (default True) If false, an error will be raised if a null value is receeved

__default__: Any (default None) If a null value is a received, it will be replaced with this

__callback__: Callable (default None) A method to call once all checks are complete.
This method receives the value as its only parameter and returns a modified value

## Float(...)

Ensures a value is a float

```python
class MySchema(Schema):
    number = Float(min_value=0.0, max_value=6.5, nullable=False, default=2.5)
```

__min_value__: float or callable returning float (default None) Minimum allowed value

__max_value__: float or callable returning float (default None) Maximum allowed value

__nullable__: bool (default True) If false, an error will be raised if a null value is receeved

__default__: Any (default None) If a null value is a received, it will be replaced with this

__callback__: Callable (default None) A method to call once all checks are complete.
This method receives the value as its only parameter and returns a modified value

## Bool(...)

Ensures a value is either true or false

```python
class MySchema(Schema):
    boolean = Bool(nullable=False, default=True)
```

__nullable__: bool (default True) If false, an error will be raised if a null value is receeved

__default__: Any (default None) If a null value is a received, it will be replaced with this

__callback__: Callable (default None) A method to call once all checks are complete.
This method receives the value as its only parameter and returns a modified value

## String(...)

Ensures a value is a string

```python
class MySchema(Schema):
    thing = String(min_length=2, max_length=5, nullable=False)
```

__min_length__: int or callable returning int (default None) Minimum allowed string length

__max_length__: int or callable returning int (default None) Maximum allowed string length

__nullable__: bool (default True) If false, an error will be raised if a null value is receeved

__default__: Any (default None) If a null value is a received, it will be replaced with this

__callback__: Callable (default None) A method to call once all checks are complete.
This method receives the value as its only parameter and returns a modified value

## Regex(...)

Ensures a value matches a regex string

```python
class MySchema(Schema):
    thing = Regex(".+@[^@]+.[^@]{2,}$", min_length=2, max_length=5, nullable=False)
```

__matcher__: regex string or compiled pattern (required) Regex to match value against

__min_length__: int or callable returning int (default None) Minimum allowed string length

__max_length__: int or callable returning int (default None) Maximum allowed string length

__nullable__: bool (default True) If false, an error will be raised if a null value is receeved

__default__: Any (default None) If a null value is a received, it will be replaced with this

__callback__: Callable (default None) A method to call once all checks are complete.
This method receives the value as its only parameter and returns a modified value

## Email(...)

Ensures a value is a valid email address

```python
class MySchema(Schema):
    thing = Email(nullable=False)
```

__min_length__: int or callable returning int (default None) Minimum allowed string length

__max_length__: int or callable returning int (default None) Maximum allowed string length

__nullable__: bool (default True) If false, an error will be raised if a null value is receeved

__default__: Any (default None) If a null value is a received, it will be replaced with this

__callback__: Callable (default None) A method to call once all checks are complete.
This method receives the value as its only parameter and returns a modified value

Notes:

- matcher used: `.+@[^@]+.[^@]{2,}$`

## Uuid(...)

Ensures a value is a valid uuid

```python
class MySchema(Schema):
    thing = Email(nullable=False, strip_hyphens=True)
```

__strip_hyphens__: bool (default False) If true, hyphens will be removed from the value string

__nullable__: bool (default True) If false, an error will be raised if a null value is receeved

__default__: Any (default None) If a null value is a received, it will be replaced with this

__callback__: Callable (default None) A method to call once all checks are complete.
This method receives the value as its only parameter and returns a modified value

Notes:

- matcher used: `^[a-fA-F0-9]{8}-?[a-fA-F0-9]{4}-?[a-fA-F0-9]{4}-?[a-fA-F0-9]{4}-?[a-fA-F0-9]{12}$`

## Date(...)

Ensures a value is either a valid iso8601 date or utc timestamp and parses to date object

```python
class MySchema(Schema):
    date = Date(nullable=False, min_value=datetime.date.today)
```

__min_value__: date or callable returning date (default None) Minimum allowed date

__max_value__: date or callable returning date (default None) Maximum allowed date

__nullable__: bool (default True) If false, an error will be raised if a null value is receeved

__default__: Any (default None) If a null value is a received, it will be replaced with this

__callback__: Callable (default None) A method to call once all checks are complete.
This method receives the value as its only parameter and returns a modified value

Notes:

- format used: `%Y-%m-%d`

## Datetime(...)

Ensures a value is a valid iso8601 datetime or utc timestamp and parses to datetime object

```python
class MySchema(Schema):
    time = DateTime(nullable=False, min_value=datetime.datetime.now)
```

__min_value__: datetime or callable returning datetime (default None) Minimum allowed datetime

__max_value__: datetime or callable returning datetime (default None) Maximum allowed datetime

__nullable__: bool (default True) If false, an error will be raised if a null value is receeved

__default__: Any (default None) If a null value is a received, it will be replaced with this

__callback__: Callable (default None) A method to call once all checks are complete.
This method receives the value as its only parameter and returns a modified value

Notes:

- format used: `%Y-%m-%dT%H:%M:%S.%f`

- accepts timezones in `hh:mm` format or `Z`

## AllOf(...)

TODO description

```python
# TODO example
```

TODO params

## AnyOf(...)

TODO description

```python
# TODO example
```

TODO params

## NoneOf(...)

TODO description

```python
# TODO example
```

TODO params

---

## Callback(...)

TODO description

```python
# TODO example
```

TODO params

---