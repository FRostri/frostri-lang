from abc import (
    ABC,
    abstractmethod,
)
from enum import (
    auto,
    Enum
)
from typing import (
    Dict,
    List,
    Optional
)

from utils.colors import TextColors
from frl.ast import (
    Block,
    Identifier,
)


class ObjectType(Enum):
    BOOLEAN = auto()
    ERROR = auto()
    FLOAT = auto()
    FUNCTION = auto()
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

    def __init__(self, outer = None):
        self._store = dict()
        self._outer = outer

    def __getitem__(self, key):
        try:
            return self._store[key]
        except KeyError as e:
            if self._outer is not None:
                return self._outer[key]

            raise e

    def __setitem__(self, key, value):
        self._store[key] = value

    def __delitem__(self, key):
        del self._store[key]


class Function(Object):

    def __init__(self,
                 parameters: List[Identifier],
                 body: Block,
                 env: Environment,
                 ident: Optional[Identifier] = None) -> None:
        self.parameters = parameters
        self.body = body
        self.env = env
        self.ident = ident

    def type(self) -> ObjectType:
        return ObjectType.FUNCTION
    
    def inspect(self) -> str:
        params: str = ', '.join([str(param) for param in self.parameters])

        if self.ident is not None:
            return 'fun {}({}) {{\n{}\n}}'.format(str(self.ident), params, str(self.body))

        return 'fun({}) {{\n{}\n}}'.format(params, str(self.body))
