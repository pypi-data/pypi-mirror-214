from enum import Enum as BaseEnum
from typing import Generic, TypeVar

T = TypeVar('T')


class Enum(BaseEnum, Generic[T]):
    """
    >>> class Color(Enum['int']):
    >>>     RED = 1, 'red'
    >>>     GREEN = 2, 'green'
    """

    def __new__(cls, value: T, label: str = None):
        if label is not None:
            assert isinstance(label, str)
        obj = object.__new__(cls)
        obj._value_ = value
        obj._label = label
        return obj

    @property
    def value(self) -> T:
        """The value of the Enum member."""
        return self._value_

    @property
    def label(self) -> str:
        return self._label or self.name

    @classmethod
    def labels(cls) -> dict[T, str]:
        return {e.value: e.label for e in cls}

    @classmethod
    def options(cls) -> tuple[tuple[T, str]]:
        return tuple((e.value, e.label) for e in cls)
