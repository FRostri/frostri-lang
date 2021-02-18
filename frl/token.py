# token.py

from enum import (
    auto,
    Enum,
    unique,
)
from typing import (
    Dict,
    NamedTuple,
)


@unique
class TokenType(Enum):
    ASSIGN = auto()  # =
    COMMA = auto()  # ,
    DIVISION = auto()  # /
    ELSE = auto()  # else
    EOF = auto()  # final del archivo
    EQ = auto()  # ==
    FALSE = auto()  # false
    FLOAT = auto()  # 3.6
    FUNCTION = auto()  # fun
    GE = auto()  # >=
    GT = auto()  # >
    IDENT = auto()  # {variable}
    IF = auto()  # if
    ILLEGAL = auto()  # Cualquier caracter que no hayamos definido
    INT = auto()  # {numero}
    LBRACE = auto()  # {
    LET = auto()  # var
    LPAREN = auto()  # (
    LE = auto()  # <=
    LT = auto()  # <
    MINUS = auto()  # -
    MULTIPLICATION = auto()  # *
    NEGATION = auto()  # !
    NOT_EQ = auto()  # !=
    PLUS = auto()  # +
    RBRACE = auto()  # }
    RETURN = auto()  # return
    RPAREN = auto()  # )
    SEMICOLON = auto()  # ;
    STRING = auto() # "un sting pue"
    TRUE = auto()  # true


class Token(NamedTuple):
    token_type: TokenType
    literal: str
    line: int = 1

    def __str__(self) -> str:
        return f'Type {self.token_type}, Literal {self.literal}'


def lookup_token_type(literal: str) -> TokenType:
    keywords: Dict[str, TokenType] = {
        'var': TokenType.LET,
        'fun': TokenType.FUNCTION,
        'if': TokenType.IF,
        'else': TokenType.ELSE,
        'false': TokenType.FALSE,
        'true': TokenType.TRUE,
        'return': TokenType.RETURN,
    }

    return keywords.get(literal, TokenType.IDENT)
