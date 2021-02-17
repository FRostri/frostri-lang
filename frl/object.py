from abc import (
    ABC,
    abstractmethod,
)
from enum import (
    auto,
    Enum
)
from typing import Dict

from utils.colors import TextColors


class ObjectType(Enum):
    BOOLEAN = auto()
    ERROR = auto()
    FLOAT = auto()
    INTEGERS = auto()
    NULL = auto()
    RETURN = auto()


class Object(ABC):

    @abstractmethod
    def type(self) -> ObjectType:
        ...

    @abstractmethod
    def inspect(self) -> str:
        ...


class Integer(Object):

    def __init__(self, value: int, line: int) -> None:
        self.value = value

    def type(self) -> ObjectType:
        return ObjectType.INTEGERS

    def inspect(self) -> str:
        return str(self.value)


class Float(Object):

    def __init__(self, value: float, line: int) -> None:
        self.value = value

    def type(self) -> ObjectType:
        return ObjectType.FLOAT

    def inspect(self) -> str:
        return str(self.value)


class Boolean(Object):

    def __init__(self, value: bool) -> None:
        self.value = value

    def type(self) -> ObjectType:
        return ObjectType.BOOLEAN

    def inspect(self) -> str:
        return 'true' if self.value else 'false'


class Null(Object):

    def type(self) -> ObjectType:
        return ObjectType.NULL

    def inspect(self) -> str:
        return 'null'


class Return(Object):

    def __init__(self, value: Object) -> None:
        self.value = value

    def type(self) -> ObjectType:
        return ObjectType.RETURN

    def inspect(self) -> str:
        return self.value.inspect()


class Error(Object):

    def __init__(self, message: str, err_code: str) -> None:
        self.message = message
        self.err_code = err_code

    def type(self) -> ObjectType:
        return ObjectType.ERROR

    def inspect(self) -> str:
        return f'{TextColors.RED}Error[{self.err_code}]{TextColors.RESET} {self.message}'


class Environment(Dict):

    def __init__(self):
        self._store = dict()

    def __getitem__(self, key):
        return self._store[key]

    def __setitem__(self, key, value):
        self._store[key] = value

    def __delitem__(self, key):
        del self._store[key]
