from unittest import TestCase

from frl.lexer import Lexer
from frl.parser import Parser
from frl.ast import Program


class ParserTest(TestCase):

    def test_pase_program(self) -> None:
        source: str = 'variable x = 5;'
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)

        program: Program = parser.parse_program()

        self.assertIsNotNone(program)
        self.assertIsInstance(program, Program)
