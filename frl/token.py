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
    ASSIGN = auto() # =
    COMMA = auto() # ,
    DIFF = auto() # !==
    DIVISION = auto() # /
    ELSE = auto() # si_no
    EOF = auto() # final del archivo
    EQ = auto() # ==
    FALSE = auto() # falso
    FUNCTION = auto() # proceso
    GE = auto() # >=
    GT = auto() # >
    IDENT = auto() # {variable}
    IF = auto() # si
    ILLEGAL = auto() # Cualquier caracter que no hayamos definido
    INT = auto() # {numero}
    LBRACE = auto() # {
    LET = auto() # var
    LPAREN = auto() # (
    LE = auto() # <=
    LT = auto() # <
    MINUS = auto() # -
    MULTIPLICATION = auto() # *
    NEGATION = auto() # !
    NOT_EQ = auto() # !=
    PLUS = auto() # +
    RBRACE = auto() # }
    RETURN = auto() # regresa
    RPAREN = auto() # )
    SEMICOLON = auto() # ;
    SIMILAR = auto() # ===
    TRUE = auto() # verdadero


class Token(NamedTuple):
    token_type: TokenType
    literal: str

    def __str__(self) -> str:
        return f'Type {self.token_type}, Literal {self.literal}'


def lookup_token_type(literal: str) -> TokenType:
    keywords: Dict[str, TokenType] = {
        'var': TokenType.LET,
        'proceso': TokenType.FUNCTION,
        'si': TokenType.IF,
        'si_no': TokenType.ELSE,
        'falso': TokenType.FALSE,
        'verdadero': TokenType.TRUE,
        'regresa': TokenType.RETURN
    }

    return keywords.get(literal, TokenType.IDENT)
