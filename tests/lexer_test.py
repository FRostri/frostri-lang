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

    def test_line_break(self) -> None:

        # Iician pegadas a las comillas de apertura porque es la línea 1, las comillas de cierre están abajo porque hay un caracter \n que igual es contado por el lexer, por eso expectamos 21 tokens
        source: str = """var cinco = 5;
                        var seis = 6;
                        var siete = 7;
                        var ocho = 8;
                        """

        lexer: Lexer = Lexer(source)

        tokens: List[Token] = []

        for i in range(21):
            tokens.append(lexer.next_token())

        expected_tokens: List[Token] = [

            Token(TokenType.LET, "var", 1),
            Token(TokenType.IDENT, "cinco", 1),
            Token(TokenType.ASSIGN, "=", 1),
            Token(TokenType.INT, "5", 1),
            Token(TokenType.SEMICOLON, ";", 1),

            Token(TokenType.LET, "var", 2),
            Token(TokenType.IDENT, "seis", 2),
            Token(TokenType.ASSIGN, "=", 2),
            Token(TokenType.INT, "6", 2),
            Token(TokenType.SEMICOLON, ";", 2),

            Token(TokenType.LET, "var", 3),
            Token(TokenType.IDENT, "siete", 3),
            Token(TokenType.ASSIGN, "=", 3),
            Token(TokenType.INT, "7", 3),
            Token(TokenType.SEMICOLON, ";", 3),

            Token(TokenType.LET, "var", 4),
            Token(TokenType.IDENT, "ocho", 4),
            Token(TokenType.ASSIGN, "=", 4),
            Token(TokenType.INT, "8", 4),
            Token(TokenType.SEMICOLON, ";", 4),

            Token(TokenType.EOF, "", 5),

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
            Token(TokenType.LET, 'var', 1),
            Token(TokenType.IDENT, 'cinco', 1),
            Token(TokenType.ASSIGN, '=', 1),
            Token(TokenType.INT, '5', 1),
            Token(TokenType.SEMICOLON, ';', 1),
        ]

        self.assertEquals(tokens, expected_tokens)

    def test_function_declaration(self) -> None:
        source: str = '''
            var suma = fun(x, y) {
                x + y;
            };
            fun resta(x, y) {
                x - y;
            };
        '''
        lexer: Lexer = Lexer(source)

        tokens: List[Token] = []
        for i in range(16):
            tokens.append(lexer.next_token())

        expected_tokens: List[Token] = [
            Token(TokenType.LET, 'var', 2),
            Token(TokenType.IDENT, 'suma', 2),
            Token(TokenType.ASSIGN, '=', 2),
            Token(TokenType.FUNCTION, 'fun', 2),
            Token(TokenType.LPAREN, '(', 2),
            Token(TokenType.IDENT, 'x', 2),
            Token(TokenType.COMMA, ',', 2),
            Token(TokenType.IDENT, 'y', 2),
            Token(TokenType.RPAREN, ')', 2),
            Token(TokenType.LBRACE, '{', 2),

            Token(TokenType.IDENT, 'x', 3),
            Token(TokenType.PLUS, '+', 3),
            Token(TokenType.IDENT, 'y', 3),
            Token(TokenType.SEMICOLON, ';', 3),

            Token(TokenType.RBRACE, '}', 4),
            Token(TokenType.SEMICOLON, ';', 4),
        ]

        self.assertEquals(tokens, expected_tokens)

    def test_function_call(self) -> None:
        source: str = 'var resultado = suma(dos, tres);'
        lexer: Lexer = Lexer(source)

        tokens: List[Token] = []
        for i in range(10):
            tokens.append(lexer.next_token())

        expected_tokens: List[Token] = [
            Token(TokenType.LET, 'var', 1),
            Token(TokenType.IDENT, 'resultado', 1),
            Token(TokenType.ASSIGN, '=', 1),
            Token(TokenType.IDENT, 'suma', 1),
            Token(TokenType.LPAREN, '(', 1),
            Token(TokenType.IDENT, 'dos', 1),
            Token(TokenType.COMMA, ',', 1),
            Token(TokenType.IDENT, 'tres', 1),
            Token(TokenType.RPAREN, ')', 1),
            Token(TokenType.SEMICOLON, ';', 1),
        ]

        self.assertEquals(tokens, expected_tokens)

    def test_control_statment(self) -> None:
        source: str = '''
            if (5 < 10) {
                return true;
            } else {
                return false;
            }
        '''
        lexer: Lexer = Lexer(source)

        tokens: List[Token] = []
        for i in range(17):
            tokens.append(lexer.next_token())

        expected_tokens: List[Token] = [
            Token(TokenType.IF, 'if', 2),
            Token(TokenType.LPAREN, '(', 2),
            Token(TokenType.INT, '5', 2),
            Token(TokenType.LT, '<', 2),
            Token(TokenType.INT, '10', 2),
            Token(TokenType.RPAREN, ')', 2),
            Token(TokenType.LBRACE, '{', 2),
            Token(TokenType.RETURN, 'return', 3),
            Token(TokenType.TRUE, 'true', 3),
            Token(TokenType.SEMICOLON, ';', 3),
            Token(TokenType.RBRACE, '}', 4),
            Token(TokenType.ELSE, 'else', 4),
            Token(TokenType.LBRACE, '{', 4),
            Token(TokenType.RETURN, 'return', 5),
            Token(TokenType.FALSE, 'false', 5),
            Token(TokenType.SEMICOLON, ';', 5),
            Token(TokenType.RBRACE, '}', 6),
        ]

        self.assertEquals(tokens, expected_tokens)

    def test_two_character_operator(self) -> None:
        source: str = '''10 == 10;
                         10 != 9;
                         10 >= 4;
                         0 <= 11;
        '''
        lexer: Lexer = Lexer(source)

        tokens: List[Token] = []
        for i in range(16):
            tokens.append(lexer.next_token())

        expected_tokens: List[Token] = [
            Token(TokenType.INT, '10', 1),
            Token(TokenType.EQ, '==', 1),
            Token(TokenType.INT, '10', 1),
            Token(TokenType.SEMICOLON, ';', 1),
            Token(TokenType.INT, '10', 2),
            Token(TokenType.NOT_EQ, '!=', 2),
            Token(TokenType.INT, '9', 2),
            Token(TokenType.SEMICOLON, ';', 2),
            Token(TokenType.INT, '10', 3),
            Token(TokenType.GE, '>=', 3),
            Token(TokenType.INT, '4', 3),
            Token(TokenType.SEMICOLON, ';', 3),
            Token(TokenType.INT, '0', 4),
            Token(TokenType.LE, '<=', 4),
            Token(TokenType.INT, '11', 4),
            Token(TokenType.SEMICOLON, ';', 4),
        ]

        self.assertEquals(tokens, expected_tokens)

    def test_identifier_with_numbers(self) -> None:
        source: str = '''var numero_1 = 5;'''
        lexer: Lexer = Lexer(source)

        tokens: List[Token] = []

        for i in range(5):
            tokens.append(lexer.next_token())

        expected_tokens: List[Token] = [
            Token(TokenType.LET, 'var', 1),
            Token(TokenType.IDENT, 'numero_1', 1),
            Token(TokenType.ASSIGN, '=', 1),
            Token(TokenType.INT, '5', 1),
            Token(TokenType.SEMICOLON, ';', 1),
        ]

        self.assertEquals(tokens, expected_tokens)

    def test_assigment_with_floats(self) -> None:
        source: str = '''
            var float_num = 1.5;
            var pepe = 4.2;
        '''
        lexer: Lexer = Lexer(source)

        tokens: List[Token] = []

        for i in range(10):
            tokens.append(lexer.next_token())

        expected_tokens: List[Token] = [
            Token(TokenType.LET, 'var', 2),
            Token(TokenType.IDENT, 'float_num', 2),
            Token(TokenType.ASSIGN, '=', 2),
            Token(TokenType.FLOAT, '1.5', 2),
            Token(TokenType.SEMICOLON, ';', 2),

            Token(TokenType.LET, 'var', 3),
            Token(TokenType.IDENT, 'pepe', 3),
            Token(TokenType.ASSIGN, '=', 3),
            Token(TokenType.FLOAT, '4.2', 3),
            Token(TokenType.SEMICOLON, ';', 3),
        ]

        self.assertEquals(tokens, expected_tokens)

    def test_string(self) -> None:
        source: str = '''
            "foo";
            \'bar\';
            "Mucho texto xddd";
        '''
        lexer: Lexer = Lexer(source)

        tokens: List[Token] = []
        for i in range(6):
            tokens.append(lexer.next_token())

        expected_tokens: List[Token] = [
            Token(TokenType.STRING, 'foo', 2),
            Token(TokenType.SEMICOLON, ';', 2),
            Token(TokenType.STRING, 'bar', 3),
            Token(TokenType.SEMICOLON, ';', 3),
            Token(TokenType.STRING, 'Mucho texto xddd', 4),
            Token(TokenType.SEMICOLON, ';', 4),
        ]

        self.assertEquals(tokens, expected_tokens)
