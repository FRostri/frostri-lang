import readline
from os import system, name
from typing import List

from frl.ast import Program
from frl.evaluator import evaluate
from frl.lexer import Lexer
from frl.object import Environment
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
    scanned: List[str] = []

    while (source := input(f'{colors.CYAN}>>{colors.RESET} ')) != 'exit()':

        if source == "clear()":
            clear()

        scanned.append(source)
        lexer: Lexer = Lexer(' '.join(scanned))
        parser: Parser = Parser(lexer)

        program: Program = parser.parse_program()
        env: Environment = Environment()

        if len(parser.errors) > 0:
            _print_parse_errors(parser.errors)
            continue

        evaluated = evaluate(program, env)

        if evaluated is not None:
            print(evaluated.inspect())
