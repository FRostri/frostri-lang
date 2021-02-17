from abc import (
    ABC,
    abstractmethod,
)
from enum import (
    auto,
    Enum
)


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

    def __init__(self, value: int) -> None:
        self.value = value

    def type(self) -> ObjectType:
        return ObjectType.INTEGERS

    def inspect(self) -> str:
        return str(self.value)


class Float(Object):

    def __init__(self, value: float) -> None:
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

    def __init__(self, message: str) -> None:
        self.message = message

    def type(self) -> ObjectType:
        return ObjectType.ERROR

    def inspect(self) -> str:
        return f'Error[0000]. {self.message}'
