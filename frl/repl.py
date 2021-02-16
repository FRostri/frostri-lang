import readline
from os import system, name
from typing import List

from frl.ast import Program
from frl.lexer import Lexer
from frl.parser import Parser
from frl.token import (
    Token,
    TokenType
)
from utils.colors import TextColors

colors = TextColors

EOF_TOKEN: Token = Token(TokenType.EOF, '')


def clear():

    # command for windows
    if name == 'nt':
        _ = system('cls')

    # commanf for mac and linux
    else:
        _ = system('clear')


def _print_parse_errors(errors: List[str]) -> None:
    for error in errors:
        print(error)


def start_repl() -> None:
    while (source := input(f'{colors.CYAN}>>{colors.RESET} ')) != 'exit()':

        if source == "clear()":
            clear()

        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)

        program: Program = parser.parse_program()

        if len(parser.errors) > 0:
            _print_parse_errors(parser.errors)
            continue

        print(program)
