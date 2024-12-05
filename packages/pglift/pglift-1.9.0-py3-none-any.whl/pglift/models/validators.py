# SPDX-FileCopyrightText: 2024 Dalibo
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from collections.abc import Sequence
from typing import TypeVar

import psycopg.conninfo
import pydantic

from ..types import Operation


def check_conninfo(value: str, exclude: Sequence[str] = ()) -> str:
    """Check that conninfo string is valid.

    Optionally checks that conninfo doesn't include provided keys.
    Sorts conninfo keys along the way.

    Raise a ValueError if conninfo is invalid.

    >>> check_conninfo("x=2")
    Traceback (most recent call last):
      ...
    ValueError: invalid connection option "x"
    <BLANKLINE>
    >>> check_conninfo("host=localhost port=5444")
    'host=localhost port=5444'
    >>> check_conninfo("host=localhost port=5444", exclude=["password", "port"])
    Traceback (most recent call last):
        ...
    ValueError: forbidden connection option 'port'
    """
    try:
        s = psycopg.conninfo.conninfo_to_dict(value)
    except psycopg.ProgrammingError as e:
        raise ValueError(str(e)) from e

    for x in exclude:
        if x in s:
            raise ValueError(f"forbidden connection option {x!r}")

    return psycopg.conninfo.make_conninfo("", **dict(sorted(s.items())))


T = TypeVar("T")


def check_mutually_exclusive_with(
    other: str,
    value: T,
    info: pydantic.ValidationInfo,
    *,
    operations: set[Operation] | None = None,
) -> T:
    """Make sure currently validated field is not specified along with 'other' field.

    If 'operations' is set, the check will happen only if the 'operation' from
    validation context matches one of specified values.
    >>> from functools import partial
    >>> from typing import Annotated
    >>>
    >>> from pydantic import AfterValidator
    >>> from ..types import BaseModel
    >>>
    >>> class Foo(BaseModel):
    ...     bar: str = ""
    ...     dude: Annotated[
    ...         str, AfterValidator(partial(check_mutually_exclusive_with, "bar"))
    ...     ] = ""
    ...     baz: Annotated[
    ...         str,
    ...         AfterValidator(
    ...             partial(check_mutually_exclusive_with, "bar", operations={"create"})
    ...         ),
    ...     ] = ""

    >>> Foo(bar="blah", dude="blah")
    Traceback (most recent call last):
      ...
    pydantic_core._pydantic_core.ValidationError: 1 validation error for Foo
    dude
      Value error, field is mutually exclusive with 'bar' [type=value_error, input_value='blah', input_type=str]
        ...

    >>> from ..types import validation_context

    >>> with validation_context(operation="update"):
    ...     Foo(bar="blah", dude="blah")
    Traceback (most recent call last):
      ...
    pydantic_core._pydantic_core.ValidationError: 1 validation error for Foo
    dude
      Value error, field is mutually exclusive with 'bar' [type=value_error, input_value='blah', input_type=str]
        ...

    >>> with validation_context(operation="update"):
    ...     Foo(bar="blah", baz="blah")
    Foo(bar='blah', dude='', baz='blah')

    >>> with validation_context(operation="create"):
    ...     Foo(bar="blah", baz="blah")
    Traceback (most recent call last):
      ...
    pydantic_core._pydantic_core.ValidationError: 1 validation error for Foo
    baz
      Value error, field is mutually exclusive with 'bar' [type=value_error, input_value='blah', input_type=str]
        ...

    Without a validation context, no validation happens:
    >>> Foo(bar="blah", baz="blah")
    Foo(bar='blah', dude='', baz='blah')

    >>> Foo(bar="blah")
    Foo(bar='blah', dude='', baz='')
    """
    if (
        value
        and info.data.get(other)
        and (
            operations is None
            or (info.context is not None and info.context["operation"] in operations)
        )
    ):
        raise ValueError(f"field is mutually exclusive with {other!r}")
    return value
