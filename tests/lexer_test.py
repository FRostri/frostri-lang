# lexer_test.py

from unittest import TestCase
from typing import List

from frl.token import (
    Token,
    TokenType,
)
from frl.lexer import Lexer


class LexerTest(TestCase):

    def test_illegal(self) -> None:
        source: str = '¡¿@'
        lexer: Lexer = Lexer(source)

        tokens: List[Token] = []
        for i in range(len(source)):
            tokens.append(lexer.next_token())

        expected_tokens: List[Token] = [
            Token(TokenType.ILLEGAL, '¡'),
            Token(TokenType.ILLEGAL, '¿'),
            Token(TokenType.ILLEGAL, '@'),
        ]

        self.assertEquals(tokens, expected_tokens)

    def test_one_character_operator(self) -> None:
        source: str = '=+-/*<>!'
        lexer: Lexer = Lexer(source)

        tokens: List[Token] = []
        for i in range(len(source)):
            tokens.append(lexer.next_token())

            expected_tokens: List[Token] = [
                Token(TokenType.ASSIGN, '='),
                Token(TokenType.PLUS, '+'),
                Token(TokenType.MINUS, "-"),
                Token(TokenType.DIVISION, "/"),
                Token(TokenType.MULTIPLICATION, "*"),
                Token(TokenType.LT, "<"),
                Token(TokenType.GT, ">"),
                Token(TokenType.NEGATION, "!"),
            ]

        self.assertEquals(tokens, expected_tokens)

    def test_eof(self) -> None:
        source: str = '+'
        lexer: Lexer = Lexer(source)

        tokens: List[Token] = []
        for i in range(len(source) + 1):
            tokens.append(lexer.next_token())

        expected_tokens: List[Token] = [
            Token(TokenType.PLUS, '+'),
            Token(TokenType.EOF, ''),
        ]

        self.assertEquals(tokens, expected_tokens)

    def test_delimeters(self) -> None:
        source: str = '(){},;'
        lexer: Lexer = Lexer(source)

        tokens: List[Token] = []
        for i in range(len(source)):
            tokens.append(lexer.next_token())

        expected_tokens: List[Token] = [
            Token(TokenType.LPAREN, '('),
            Token(TokenType.RPAREN, ')'),
            Token(TokenType.LBRACE, '{'),
            Token(TokenType.RBRACE, '}'),
            Token(TokenType.COMMA, ','),
            Token(TokenType.SEMICOLON, ';'),
        ]

        self.assertEquals(tokens, expected_tokens)

    def test_assigment(self) -> None:
        source: str = 'var cinco = 5;'
        lexer: Lexer = Lexer(source)

        tokens: List[Token] = []
        for i in range(5):
            tokens.append(lexer.next_token())

        expected_tokens: List[Token] = [
            Token(TokenType.LET, 'var'),
            Token(TokenType.IDENT, 'cinco'),
            Token(TokenType.ASSIGN, '='),
            Token(TokenType.INT, '5'),
            Token(TokenType.SEMICOLON, ';'),
        ]

        self.assertEquals(tokens, expected_tokens)

    def test_function_declaration(self) -> None:
        source: str = '''
            var suma = proceso(x, y) {
                x + y;
            };
        '''
        lexer: Lexer = Lexer(source)

        tokens: List[Token] = []
        for i in range(16):
            tokens.append(lexer.next_token())

        expected_tokens: List[Token] = [
            Token(TokenType.LET, 'var'),
            Token(TokenType.IDENT, 'suma'),
            Token(TokenType.ASSIGN, '='),
            Token(TokenType.FUNCTION, 'proceso'),
            Token(TokenType.LPAREN, '('),
            Token(TokenType.IDENT, 'x'),
            Token(TokenType.COMMA, ','),
            Token(TokenType.IDENT, 'y'),
            Token(TokenType.RPAREN, ')'),
            Token(TokenType.LBRACE, '{'),
            Token(TokenType.IDENT, 'x'),
            Token(TokenType.PLUS, '+'),
            Token(TokenType.IDENT, 'y'),
            Token(TokenType.SEMICOLON, ';'),
            Token(TokenType.RBRACE, '}'),
            Token(TokenType.SEMICOLON, ';'),
        ]

        self.assertEquals(tokens, expected_tokens)

    def test_function_call(self) -> None:
        source: str = 'var resultado = suma(dos, tres);'
        lexer: Lexer = Lexer(source)

        tokens: List[Token] = []
        for i in range(10):
            tokens.append(lexer.next_token())

        expected_tokens: List[Token] = [
            Token(TokenType.LET, 'var'),
            Token(TokenType.IDENT, 'resultado'),
            Token(TokenType.ASSIGN, '='),
            Token(TokenType.IDENT, 'suma'),
            Token(TokenType.LPAREN, '('),
            Token(TokenType.IDENT, 'dos'),
            Token(TokenType.COMMA, ','),
            Token(TokenType.IDENT, 'tres'),
            Token(TokenType.RPAREN, ')'),
            Token(TokenType.SEMICOLON, ';'),
        ]

        self.assertEquals(tokens, expected_tokens)

    def test_control_statment(self) -> None:
        source: str = '''
            si (5 < 10) {
                regresa verdadero;
            } si_no {
                regresa falso;
            }
        '''
        lexer: Lexer = Lexer(source)

        tokens: List[Token] = []
        for i in range(17):
            tokens.append(lexer.next_token())

        expected_tokens: List[Token] = [
            Token(TokenType.IF, 'si'),
            Token(TokenType.LPAREN, '('),
            Token(TokenType.INT, '5'),
            Token(TokenType.LT, '<'),
            Token(TokenType.INT, '10'),
            Token(TokenType.RPAREN, ')'),
            Token(TokenType.LBRACE, '{'),
            Token(TokenType.RETURN, 'regresa'),
            Token(TokenType.TRUE, 'verdadero'),
            Token(TokenType.SEMICOLON, ';'),
            Token(TokenType.RBRACE, '}'),
            Token(TokenType.ELSE, 'si_no'),
            Token(TokenType.LBRACE, '{'),
            Token(TokenType.RETURN, 'regresa'),
            Token(TokenType.FALSE, 'falso'),
            Token(TokenType.SEMICOLON, ';'),
            Token(TokenType.RBRACE, '}'),
        ]

        self.assertEquals(tokens, expected_tokens)

    def test_two_character_operator(self) -> None:
        source: str = '''
            10 == 10;
            10 != 9;
            10 >= 4;
            0 <= 11;
        '''
        lexer: Lexer = Lexer(source)

        tokens: List[Token] = []
        for i in range(16):
            tokens.append(lexer.next_token())

        expected_tokens: List[Token] = [
                Token(TokenType.INT, '10'),
                Token(TokenType.EQ, '=='),
                Token(TokenType.INT, '10'),
                Token(TokenType.SEMICOLON, ';'),
                Token(TokenType.INT, '10'),
                Token(TokenType.NOT_EQ, '!='),
                Token(TokenType.INT, '9'),
                Token(TokenType.SEMICOLON, ';'),
                Token(TokenType.INT, '10'),
                Token(TokenType.GE, '>='),
                Token(TokenType.INT, '4'),
                Token(TokenType.SEMICOLON, ';'),
                Token(TokenType.INT, '0'),
                Token(TokenType.LE, '<='),
                Token(TokenType.INT, '11'),
                Token(TokenType.SEMICOLON, ';'),
        ]

        self.assertEquals(tokens, expected_tokens)

    def test_three_character_operator(self) -> None:
        source: str = '''
            10 === 10;
            9 !== 4;
        '''
        lexer: Lexer = Lexer(source)

        tokens: List[Token] = []
        for i in range(8):
            tokens.append(lexer.next_token())

        expected_tokens: List[Token] = [
            Token(TokenType.INT, '10'),
            Token(TokenType.SIMILAR, '==='),
            Token(TokenType.INT, '10'),
            Token(TokenType.SEMICOLON, ';'),
            Token(TokenType.INT, '9'),
            Token(TokenType.DIFF, '!=='),
            Token(TokenType.INT, '4'),
            Token(TokenType.SEMICOLON, ';'),
        ]

        self.assertEquals(tokens, expected_tokens)

    def test_mixed_character_operator(self) -> None:

        source: str = """
            10 === 10;
            10 !== 9;
            10 == 10;
            10 != 9;
        """

        lexer: Lexer = Lexer(source)

        tokens: List[Token] = []

        for i in range(16):

            tokens.append(lexer.next_token())

        expected_tokens: List[Token] = [
            Token(TokenType.INT, "10"),
            Token(TokenType.SIMILAR, "==="),
            Token(TokenType.INT, "10"),
            Token(TokenType.SEMICOLON, ";"),
            Token(TokenType.INT, "10"),
            Token(TokenType.DIFF, "!=="),
            Token(TokenType.INT, "9"),
            Token(TokenType.SEMICOLON, ";"),
            Token(TokenType.INT, "10"),
            Token(TokenType.EQ, "=="),
            Token(TokenType.INT, "10"),
            Token(TokenType.SEMICOLON, ";"),
            Token(TokenType.INT, "10"),
            Token(TokenType.NOT_EQ, "!="),
            Token(TokenType.INT, "9"),
            Token(TokenType.SEMICOLON, ";"),
        ]

        self.assertEquals(tokens, expected_tokens)

    def test_identifier_with_numbers(self) -> None:
        source: str = '''
            var numero_1 = 5;
        '''
        lexer: Lexer = Lexer(source)

        tokens: List[Token] = []

        for i in range(5):
            tokens.append(lexer.next_token())

        expected_tokens: List[Token] = [
            Token(TokenType.LET, 'var'),
            Token(TokenType.IDENT, 'numero_1'),
            Token(TokenType.ASSIGN, '='),
            Token(TokenType.INT, '5'),
            Token(TokenType.SEMICOLON, ';'),
        ]
