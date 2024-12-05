Examples
========

Objects
-------

Three different kinds of objects are supported to be loaded and dumped back.

* NamedTuple (stdlib)
* dataclass (stdlib)
* attrs (3rd party module)

More or less they all work in the same way: the object is defined, types are assigned for the fields and typedload can inspect the class and create an instance from a dictionary, or go the other way to a dictionary from an instance.

```python
from typing import NamedTuple
from pathlib import Path
import typedload
from attr import attrs, attrib

class File(NamedTuple):
    path: Path
    size: int

@attrs
class Directory:
    name = str
    files: list[File] = attrib(factory=list) # mutable objects require a factory, not a default value

dir = {
    'name': 'home',
    'files': [
        {'path': '/asd.txt', 'size': 0},
        {'path': '/tmp/test.txt', 'size': 30},
    ]
}

# Load the dictionary into objects
d = typedload.load(dir, Directory)
# Out: Directory(files=[File(path='/asd.txt', size=0), File(path='/tmp/test.txt', size=30)])

# Dump the objects into a dictionary
typedload.dump(d)
```

Loading with optional and default values
----------------------------------------

Python typing is confusing for many concerning the meaning of `Optional`. An `Optional[T]` means that the field can assume `None` as value, but the value must still be specified, and can't be omitted. If, on the other hand, a variable has a default value, then when it's not explicitly specified, the default value is assumed.

Typedload follows exactly the normal behaviour of python and mypy.

With the new syntax, writing `Optional[int]` is equivalent to `int | None`.


```python
import typedload
from typing import Optional, NamedTuple

class User(NamedTuple):
    username: str # Must be assigned
    nickname: Optional[str] # Must be assigned and can be None
    last_login: Optional[int] = None # Not required.

# This fails, as nickname is not present
typedload.load({'username': 'ltworf'}, User)
# TypedloadValueError: Value does not contain fields: {'nickname'} which are necessary for type User

# Those 2 work fine
typedload.load({'username': 'ltworf', 'nickname': None}, User)
# Out: User(username='ltworf', nickname=None, last_login=None)

typedload.load({'username': 'ltworf', 'nickname': 'LtWorf'}, User)
# Out: User(username='ltworf', nickname='LtWorf', last_login=None)

# Those 2 work fine too
typedload.load({'username': 'ltworf', 'nickname': None, 'last_login': None}, User)
# Out: User(username='ltworf', nickname=None, last_login=None)

typedload.load({'username': 'ltworf', 'nickname': None, 'last_login': 666}, User)
# Out: User(username='ltworf', nickname=None, last_login=666)
```

There is of course no relationship between a default value and `Optional`, so a default can be anything. The following is valid:

```python
class A(NamedTuple):
    # The field can be None, but if not specified it defaults to 3
    i: Optional[int] = 3
```

Dumping with optional and default values
----------------------------------------

```python
class Coordinates(NamedTuple):
    x: int = 0
    y: int = 0
```

When dumping values, the fields which match with their default value are omitted.

```python
# Returns an empty dictionary
typedload.dump(Coordinates())
# Out: {}


# Returns only the x value
typedload.dump(Coordinates(x=42, y=0))
# Out: {'x': 42}

# To emit all the fields, including those that are using the default one
# set hidedefault=False
typedload.dump(Coordinates(), hidedefault=False)
# Out: {'x': 0, 'y': 0}
```

Tagged unions
-------------

A typical case for unions of object is to have a *type* field that type the object itself, in a string.

This makes conflicts impossible and so in the union the correct type will always be picked.

*This is very fast, because typedload will internally use the `Literal` as an index to find the correct class.*

For example, Slack sends events in this way.

```python
import typedload
from typing import List, Literal, Union, NamedTuple

events = [
    {
    "type": "message",
    "text": "hello"
    },
    {
    "type": "user-joined",
    "username": "giufà"
    }
]

# We have events that can be of many types

class Message(NamedTuple):
    type: Literal['message']
    text: str

class UserJoined(NamedTuple):
    type: Literal['user-joined']
    username: str

# Now to load our event list
typedload.load(events, List[Union[Message, UserJoined]])
# Out: [Message(type='message', text='hello'), UserJoined(type='user-joined', username='giufà')]
```

As usual, extra fields are ignored by default. If you want to be more strict, enable `failonextra=True`.


Untagged unions
---------------

Untagged unions are not a very common feature among libraries, but typedload supports them.

Of course the problem is that if a value can be loaded into more than one type in the union, the result is not deterministic.

For example, using objects where all the fields have a default value is a bad idea:

```python
import typedload
from typing import NamedTuple, Union, Optional

class Person(NamedTuple):
    name: str = ''

class Data(NamedTuple):
    data: Optional[str] = None

# WARNING: This might return either a Person or a Data. It's random
typedload.load({}, Union[Person, Data])
# Out: Data(data=None)
# Out: Person(name='')
```

To detect the situation, we can use `uniondebugconflict=True`

```python
typedload.load({}, Union[Person, Data], uniondebugconflict=True)
# Out: TypedloadTypeError: Value of dict could be loaded into Union 2 times
```

This option is intended only for debug, since it will make typedload slower.


### failonextra

You might want to use `failonextra` for objects whose fields are subset of other objects.

```python
import typedload
from typing import NamedTuple, Union


class Person(NamedTuple):
    name: str

class Car(NamedTuple):
    name: str
    model: str

# This should be a Car, not a Person
data = {'name': 'macchina', 'model': 'TP21'}

# WARNING: This can return either a Person or a Car
typedload.load(data, Union[Person, Car])
# Out: Person(name='macchina')
# Out: Car(name='macchina', model='TP21')

# This can be explained by checking that both of these work

typedload.load(data, Person)
# Out: Person(name='macchina')

typedload.load(data, Car)
# Out: Car(name='macchina', model='TP21')

# The data we have works for both objects, and the union
# picks the first one (python sorts them randomly)

# We want to avoid that dictionary to be loaded as Person, so we use failonextra

# This fails
typedload.load(data, Person, failonextra=True)
# TypedloadValueError: Dictionary has unrecognized fields: model and cannot be loaded into Person

# This works
typedload.load(data, Car, failonextra=True)
# Out: Car(name='macchina', model='TP21')

# At this point the union will reliably pick the class that we want
typedload.load(data, Union[Person, Car], failonextra=True)
# Out: Car(name='macchina', model='TP21')
```

Disable cast loading unions
---------------------------

Many times it is beneficial to disable casting when loading.

For example, if a value can be an object of a certain kind or a string, not disabling casting will cast any invalid object to a string, which might not be desired.

```python
import typedload
from typing import NamedTuple, Union

class Data(NamedTuple):
    data: int

# This loads "{'date': 33}", since the object is not a valid Data object.
typedload.load({'date': 33}, Union[str, Data])
# Out: "{'date': 33}"

# This fails, because the dictionary is not cast to str
typedload.load({'date': 33}, Union[str, Data], basiccast=False)
# TypedloadValueError: Value of dict could not be loaded into typing.Union[str, __main__.Data]
```

list[T] | T
-----------

Some terribly evil programmers use json in this way:

* A list in case they have multiple values
* A single object in case they have one value
* Nothing at all in case they have zero values

Let's see how typedload can help us survive the situation without having to handle all the cases every time.

```python
import typedload
from typing import NamedTuple, Union, List
import dataclasses

# Multiple data points, a list is used
data0 = {
    "data_points": [{"x": 1.4, "y": 4.1}, {"x": 5.2, "y": 6.13}]
}

# A single data point. Instead of a list of 1 element, the element is passed directly
data1 = {
    "data_points": {"x": 1.4, "y": 4.1}
}

# No data points. Instead of an empty list, the object is empty
data2 = {}

# Now we make our objects
class Point(NamedTuple):
    x: float
    y: float

@dataclasses.dataclass
class Data:
    # We make an hidden field to load the data_points field from the json
    # If the value is absent it will default to an empty list
    # The hidden field can either be a List[Point] or directly a Point object
    _data_points: Point | list[Point] = dataclasses.field(default_factory=list, metadata={'name': 'data_points'})

    @property
    def data_points(self) -> List[Point]:
        # We make a property called data_points, that always returns a list
        if not isinstance(self._data_points, list):
            return [self._data_points]
        return self._data_points

# Now we can load our data, and they will all be lists of Point
typedload.load(data0, Data).data_points
# Out: [Point(x=1.4, y=4.1), Point(x=5.2, y=6.13)]

typedload.load(data1, Data).data_points
# Out: [Point(x=1.4, y=4.1)]

typedload.load(data2, Data).data_points
# Out: []
```

Name mangling
-------------

Name mangling is primarily used to deal with camel-case in codebases that use snake_case.

It is supported using `dataclass` and `attrs`, which provide metadata for the fields.

Let's assume that our original data uses camel case.

Since we are not maniacs, we want the fields in python to use snake_case, we do the following:

```python
from dataclasses import dataclass, field
import typedload

@dataclass
class Character:
    first_name: str = field(metadata={'name': 'firstName'})
    last_name: str = field(metadata={'name': 'lastName'})

data = {"firstName": "Paolino", "lastName": "Paperino"}

character = typedload.load(data, Character)
# Out: Character(first_name='Paolino', last_name='Paperino')
```

When dumping back the data

```python
typedload.dump(character)
# Out: {'lastName': 'Paperino', 'firstName': 'Paolino'}
```

the names will be converted back to camel case.


Multiple name mangling schemes
------------------------------

If we want to load from a source and dump to another source that uses a different convention, we can use `mangle_key`

```python
from dataclasses import dataclass, field
import typedload

@dataclass
class Character:
    first_name: str = field(metadata={'name': 'firstName', 'alt_name': 'first-name'})
    last_name: str = field(metadata={'name': 'lastName', 'alt_name': 'last-name'})

data = {"firstName": "Paolino", "lastName": "Paperino"}

character = typedload.load(data, Character)
# Out: Character(first_name='Paolino', last_name='Paperino')

typedload.dump(character, mangle_key='alt_name')
# Out: {'last-name': 'Paperino', 'first-name': 'Paolino'}
```

Load and dump types from str
----------------------------

Some classes are easy to load and dump from `str`. For example this is done for `Path`.

Let's assume we want to have a class that is called `SerialNumber` that we load from a string and dump back to a string.

Here's how it can be done:

```python
from typing import List
import typedload.datadumper
import typedload.dataloader

class SerialNumber:
    def __init__(self, sn: str) -> None:
        # Some validation
        if ' ' in sn:
            raise Exception('Invalid serial number')

        self.sn = sn

    def __str__(self):
        return self.sn

l = typedload.dataloader.Loader()
d = typedload.datadumper.Dumper()
l.strconstructed.add(SerialNumber)
d.strconstructed.add(SerialNumber)

serials = l.load(['1', '2', '3'], List[SerialNumber])
d.dump(serials)
```

Custom handlers
---------------

Let's assume that our codebase uses methods `from_json()` and `to_json()` as custom methods, and we want to use those.

```python
from typing import NamedTuple
import typedload.datadumper
import typedload.dataloader
import typedload.exceptions

# This is a NamedTuple, but we want to give priority to the from/to json methods
class Point(NamedTuple):
    x: int
    y: int

    @staticmethod
    def from_json(data):
        # Checks on the data
        # Typedload handlers must raise subclasses of TypedloadException to work properly
        if not isinstance(data, list):
            raise typedload.exceptions.TypedloadTypeError('List expected')
        if len(data) != 2:
            raise typedload.exceptions.TypedloadTypeError('Only 2 items')
        if not all(isinstance(i, int) for i in data):
            raise typedload.exceptions.TypedloadValueError('Values must be int')

        # Return the data
        return Point(*data)

    def to_json(self):
        return [self.x, self.y]

# We get a loader
l = typedload.dataloader.Loader()

# We find which handler handles NamedTuple
nt_handler = l.index(Point)

# We prepare a new handler
load_handler = (
    lambda x: hasattr(x, 'from_json'), # Anything that has a from_json
    lambda loader, value, type_: type_.from_json(value) # Call the from_json and return its value
)

# We add the new handler
l.handlers.insert(nt_handler, load_handler)

# Ready to try it!
l.load([1, 2], Point)
# Out: Point(x=1, y=2)

# Now we do the dumper
d = typedload.datadumper.Dumper()
nt_handler = d.index(Point(1,2)) # We need to use a real object to find the handler

dump_handler = (
    lambda x: hasattr(x, 'from_json'), # Anything that has a from_json
    lambda dumper, value, value_type: value.to_json() # Call the from_json and return its value
)
d.handlers.insert(nt_handler, dump_handler)

d.dump(Point(5, 5))
# Out: [5, 5]
```

Handlers basically permit doing anything, replacing current handlers or adding more to deal with more types.

You can just append them to the list if you are extending.

Remember to always use typedload exceptions, implement checks, and never modify the handler list after loading or dumping something.

TypedDict with total and required
---------------------------------

With TypedDict, when using `total`, it is possible to mix `Required` and `NotRequired` to change the behaviour for one field.

```python
class A(TypedDict, total=True):
    a: int
    b: int
    c: NotRequired[int]
    d: NotRequired[int]

class B(TypedDict, total=False):
    a: Required[int]
    b: Required[int]
    c: int
    d: int
```
