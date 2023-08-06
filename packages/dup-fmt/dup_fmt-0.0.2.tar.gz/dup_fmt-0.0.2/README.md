# Data Utility Package: *Formatter*

[![test](https://github.com/korawica/dup-fmt/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/korawica/dup-fmt/actions/workflows/tests.yml)
[![codecov](https://codecov.io/gh/korawica/dup-fmt/branch/main/graph/badge.svg?token=J2MN63IFT0)](https://codecov.io/gh/korawica/dup-fmt)
[![python support version](https://img.shields.io/pypi/pyversions/dup-fmt)](https://pypi.org/project/dup-fmt/)
[![size](https://img.shields.io/github/languages/code-size/korawica/dup-fmt)](https://github.com/korawica/dup-fmt)

**Type**: `DUP` | **Tag**: `Data Utility Package` `Data` `Utility`

**Table of Contents**:

- [Formatter Objects](#formatter-objects)
  - [Datetime](#datetime)
  - [Version](#version)
  - [Serial](#serial)
  - [Naming](#naming)
  - [Constant](#constant)
- [Ordered Formatter](#ordered-formatter)
- [Formatter Group](#formatter-group)
- [Make your Formatter Object](#make-your-formatter-object)

This **Formatter** package was created for `parse` and `format` any string values
that able to design format pattern with regular expression. This package be the
co-pylot project for stating to my Python software developer role.

**Install from PyPI**:

```shell
pip install dup-fmt
```

First objective of this project is include necessary formatter objects for data
components of the framework engine pakage. We can use `parse` any filename on source
server machine and ingest the right filename to target landing zone.

For example, we want to get filename with the format like, `filename_20220101.csv`, on
the file system storage, and we want to incremental ingest latest file with date **2022-03-25**
date. So we will implement `Datetime` object and parse that filename to it,

```python
Datetime.parse('filename_20220101.csv', 'filename_%Y%m%d.csv').value == datetime.today()
```

The above example is **NOT SURPRISE!!!** for us because Python already provide build-in package
`datetime` to parse by `.strptime` and format by `.strftime` with any string datetime value.
This package will the special thing when we combine more than one formatter objects such as `Naming`,
`Version`, or `Constant` together.

**For complex filename format like**:

```text
{filename:%s}_{datetime:%Y_%m_%d}.{version:%m.%n.%c}.csv
```

From above format filename, the `datetime` package does not enough for this scenario right?
but you can handle by your hard-code object or create the better package than this project.

> **Note**: \
> Any formatter object was implemented the `self.valid` method for help us validate
> target string value like the above example scenario,
> ```python
> this_date = Datetime.parse('20220101', '%Y%m%d')
> this_date.valid('any_files_20220101.csv', 'any_files_%Y%m%d.csv')  # True
> ```

## Formatter Objects

- [Datetime](#datetime)
- [Version](#version)
- [Serial](#serial)
- [Naming](#naming)
- [Constant](#constant)

The main component is **Formatter Objects** for `parse` and `format` with string
value, such as `Datetime`, `Version`, and `Serial` formatter objects. This objects
were used for parse any filename with put the format string value. The formatter
able to enhancement any format value from sting value, like in `Datetime`, for `%B`
value that was designed for month shortname (`Jan`, `Feb`, etc.) that does not
support in build-in `datetime` package.

> **Note**: \
> The main usage of this formatter object is `parse` and `format` method.

### Datetime

```python
from dup_fmt import Datetime

datetime = Datetime.parse(
   value='This_is_time_20220101_000101',
   fmt='This_is_time_%Y%m%d_%H%M%S'
)
datetime.format('This_datetime_format_%Y%b-%-d_%H:%M:%S')
```

```text
>>> 'This_datetime_format_2022Jan-1_00:01:01'
```

### Version

```python
from dup_fmt import Version

version = Version.parse(
    value='This_is_version_2_0_1',
    fmt='This_is_version_%m_%n_%c',
)
version.format('New_version_%m%n%c')
```

```text
>>> 'New_version_201'
```

### Serial

```python
from dup_fmt import Serial

serial = Serial.parse(
    value='This_is_serial_62130',
    fmt='This_is_serial_%n'
)
serial.format('Convert to binary: %b')
```

```text
>>> 'Convert to binary: 1111001010110010'
```

### Naming

```python
from dup_fmt import Naming

naming = Naming.parse(
    value='de is data engineer',
    fmt='%a is %n'
)
naming.format('Camel case is %c')
```

```text
>>> 'Camel case is dataEngineer'
```

### Constant

```python
from dup_fmt import Constant
from dup_fmt.errors import FormatterError

const = Constant({
    '%n': 'normal',
    '%s': 'special',
})
try:
    parse_const = const.parse(
        value='This_is_constant_normal',
        fmt='This_is_constant_%n'
    )
    parse_const.format('The value of %%s is %s')
except FormatterError as err:
    print(err)
```

```text
>>> 'The value of %s is special'
```

> **Note**: \
> This package already implement environment constant object, `dup_fmt.EnvConstant`.

## Ordered Formatter

The Formatter object already implement the `OrderFormatter` object that combine
all formatter objects together and can use order properties with other
`OrderFormatter` object.

```python
from dup_fmt import OrderFormatter, Datetime, Version

ordered_1 = OrderFormatter({
    'timestamp': Datetime.parse("20220101", "%Y%m%d"),
    'version': Version.parse("202", "%m%n%c"),
})
ordered_2 = OrderFormatter({
    'timestamp': {"value": "20220101", "fmt": "%Y%m%d"},
    'version': Version.parse("201", "%m%n%c"),
})
assert ordered_1 > ordered_2
```

> **Warning**: \
> This object support for any formatter object only in `FORMATTERS` mapping constant,
> this mapping constant contain; `Datetime` - timestamp, `Serial` - serial,
> `Version` - version, `Naming` - naming, and `EnvConstant` - envconst.

## Formatter Group

The formatter group object, `FormatterGroup`, that is the grouping of needed
mapping formatter object and name together. You can define a name of formatter
like `name` as Naming object, or `timestamp` as Datetime object.

**Parse**:

```python
from dup_fmt import FormatterGroup, Naming, Datetime

group = FormatterGroup({'name': Naming, 'datetime': Datetime})
group.parser(
    'data_engineer_in_20220101_de',
    fmt='{name:%s}_in_{timestamp:%Y%m%d}_{name:%a}',
    _max=False
)
```

```text
>>> {
>>>     'name': Naming.parse('data engineer', '%n'),
>>>     'timestamp': Datetime.parse('2022-01-01 00:00:00.000000', '%Y-%m-%d %H:%M:%S.%f')
>>> }
```

> **Note**: \
> The `_max` option is the max strategy for pick the maximum level from duplication
> formats in parser method. If set this value to `False` it will use the combine
> strategy for combine all duplicated formats together before parsing.

**Format**:

```python
from dup_fmt import FormatterGroup, Naming, Datetime
from datetime import datetime

group = FormatterGroup({
    'name': {'fmt': Naming, 'value': 'data engineer'},
    'datetime': {'fmt': Datetime, 'value': datetime(2022, 1, 1)}
})
group.format('{name:%c}_{timestamp:%Y_%m_%d}_{name}')
```

```text
>>> dataEngineer_2022_01_01
```

## Make your Formatter Object

If this implemented formatter objects in this package does not help you all scenario
of a formatted value, you can create your formatter object by yourself.

This package provide the base abstract class, `BaseFormatter`, for this use-case. You
can create your formatter object like,

```python
from typing import Optional, Dict, Union, Callable, Tuple
from dup_fmt import BaseFormatter


class Storage(BaseFormatter):

    base_fmt = '%b'

    base_attr_prefix = "st"

    __slots__ = (
        "_st_bit",
        "_st_byte",
        "_st_storge",
    )

    @property
    def value(self) -> int:
        return int(self.string)

    @property
    def string(self) -> str:
        return self._st_bit

    @property
    def priorities(self) -> Dict[
        str, Dict[str, Union[Callable, Tuple[int, ...], int]]
    ]:
        return {
            "bit": {
                "value": lambda x: str(x),
                "level": 1,
            },
            "byte": {
                "value": lambda x: str(int(x.replace('B', '')) * 8),
                "level": 1,
            },
            "bit_default": {"value": self.default("0")},
            "byte_default": {"value": self.default("0")}
        }

    @staticmethod
    def formatter(
            value: Optional[int] = None,
    ) -> Dict[str, Dict[str, Union[Callable, str]]]:
        """Generate formatter that support mapping formatter,
            %b  : Bit format
            %B  : Byte format
        """
        size: int = value or 0
        return {
            '%b': {
                'value': lambda: str(size),
                "regex": r"(?P<bit>[0-9]*)",
            },
            '%B': {
                'value': lambda: f"{str(round(size / 8))}B",
                'regex': r"(?P<byte>[0-9]*B)",
            }
        }

Storage({'bit': 2000}).format('%B')
```

```text
>>> 250B
```

Read more about [API Document](/docs/en//docs/API.md).

## License

This project was licensed under the terms of the [MIT license](LICENSE).
