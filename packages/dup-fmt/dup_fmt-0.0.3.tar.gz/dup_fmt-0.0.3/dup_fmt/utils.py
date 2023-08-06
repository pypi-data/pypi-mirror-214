from __future__ import annotations

from typing import Any, Callable, Iterable, List, Union

concat: Callable[[Union[List[str], Iterable[str]]], str] = "".join


def remove_pad(value: str) -> str:
    """Remove zero padding of string
    .. usage::
        >>> remove_pad('000')
        '0'

        >>> remove_pad('010')
        '10'

        >>> remove_pad('0123')
        '123'
    """
    return value.lstrip("0") or "0"


def itself(x: Any = None) -> Any:
    """Return itself value"""
    return x


def caller(func: Union[Callable[[], Any], Any]) -> Any:
    """Call function if it was callable
    .. usage::
        >>> some_func = lambda: 100
        >>> caller(some_func)
        100
    """
    return func() if callable(func) else func
