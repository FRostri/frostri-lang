from unittest import TestCase

from frl.ast import (
    Identifier,
    Integer,
    LetStatement,
    ReturnStatement,
    Program,
)
from frl.token import (
    Token,
    TokenType,
)


class ASTTest(TestCase):

    def test_let_statement(self) -> None:
        program: Program = Program(statements=[
            LetStatement(
                token=Token(TokenType.LET, literal='var'),
                name=Identifier(
                    token=Token(TokenType.IDENT, literal='mi_var'),
                    value='mi_var'
                ),
                value=Identifier(
                    token=Token(TokenType.IDENT, literal='otra_variable'),
                    value='otra_var'
                )
            )
        ])

        program_str = str(program)

        self.assertEquals(program_str, 'var mi_var = otra_var;')

    def test_return_statement(self) -> None:
        program: Program = Program(statements=[
            ReturnStatement(
                token=Token(TokenType.RETURN, literal="regresa"),
                return_value=Identifier(
                    token=Token(TokenType.IDENT, literal="mi_var"),
                    value='mi_var'
                )
            )
        ])

        program_str = str(program)

        self.assertEquals(program_str, 'regresa mi_var;')

    def test_integer_in_let_and_return_statement(self) -> None:
        program: Program = Program(statements=[
            LetStatement(
                token=Token(
                    TokenType.LET,
                    literal="var"
                ),
                name=Identifier(
                    token=Token(TokenType.IDENT, literal="mi_num"),
                    value="mi_num"
                ),
                value=Integer(
                    token=Token(TokenType.INT, literal="5"),
                    value=5
                )
            ),
            ReturnStatement(
                token=Token(TokenType.RETURN, literal="regresa"),
                return_value=Identifier(
                    token=Token(TokenType.IDENT, literal="mi_num"),
                    value="mi_num"
                )
            )
        ])

        program_str = str(program)

        self.assertEquals(program_str, 'var mi_num = 5;regresa mi_num;')
