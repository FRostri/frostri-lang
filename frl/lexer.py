# lexer.py

from re import match

from frl.token import (
    Token,
    TokenType,
    lookup_token_type,
)


class Lexer:

    def __init__(self, source: str) -> None:
        self._source: str = source
        self._character: str = ''
        self._read_position: int = 0
        self._position: int = 0

        self._read_character()

    def next_token(self) -> Token:
        self._skip_whitespace()
        # Token '='
        if match(r'^=$', self._character):
            if self._peek_character() == '=':
                token = self._make_two_character_token(TokenType.EQ)
            else:
                token = Token(TokenType.ASSIGN, self._character)
        # Token '+'
        elif match(r'^\+$', self._character):
            token = Token(TokenType.PLUS, self._character)
        # Token '-'
        elif match(r'^-$', self._character):
            token = Token(TokenType.MINUS, self._character)
        # Token '*'
        elif match(r'^\*$', self._character):
            token = Token(TokenType.MULTIPLICATION, self._character)
        # Token '/'
        elif match(r'^\/$', self._character):
            token = Token(TokenType.DIVISION, self._character)
        # Token ''
        elif match(r'^$', self._character):
            token = Token(TokenType.EOF, self._character)
        # Token '('
        elif match(r'^\($', self._character):
            token = Token(TokenType.LPAREN, self._character)
        # Token ')'
        elif match(r'^\)$', self._character):
            token = Token(TokenType.RPAREN, self._character)
        # Token '{'
        elif match(r'^\{$', self._character):
            token = Token(TokenType.LBRACE, self._character)
        # Token '}'
        elif match(r'^\}$', self._character):
            token = Token(TokenType.RBRACE, self._character)
        # Token ','
        elif match(r'^\,$', self._character):
            token = Token(TokenType.COMMA, self._character)
        # Token ';'
        elif match(r'^\;$', self._character):
            token = Token(TokenType.SEMICOLON, self._character)
        # Token '<'
        elif match(r'^<$', self._character):
            if self._peek_character() == '=':
                token = self._make_two_character_token(TokenType.LE)
            else:
                token = Token(TokenType.LT, self._character)
        # Token '>'
        elif match(r'^>$', self._character):
            if self._peek_character() == '=':
                token = self._make_two_character_token(TokenType.GE)
            else:
                token = Token(TokenType.GT, self._character)
        # Token '!'
        elif match(r'^!$', self._character):
            if self._peek_character() == '=':
                token = self._make_two_character_token(TokenType.NOT_EQ)
            else:
                token = Token(TokenType.NEGATION, self._character)
        # Token for any letter
        elif self._is_letter(self._character):
            literal = self._read_identifier()
            token_type = lookup_token_type(literal)

            return Token(token_type, literal)
        # Token for read numbers
        elif self._is_number(self._character):
            literal = self._read_number()

            if self._character == '.':
                self._read_character()
                sufix = self._read_number()
                return Token(TokenType.FLOAT, f'{literal}.{sufix}')

            return Token(TokenType.INT, literal)
        # Illegal Token
        else:
            token = Token(TokenType.ILLEGAL, self._character)
        self._read_character()

        return token

    def _is_letter(self, character: str) -> bool:
        # Expresión regular para obtener todas las letras del alfabeto español
        return bool(match(r'^[a-zA-Z_]$', character))

    def _is_number(self, character: str) -> bool:
        # Expresión regular para objeter todos los digitos
        return bool(match(r'^\d$', character))

    def _make_two_character_token(self, token_type: TokenType) -> Token:
        prefix = self._character
        self._read_character()
        suffix = self._character

        return Token(token_type, f'{prefix}{suffix}')

    def _read_character(self) -> None:
        if self._read_position >= len(self._source):
            self._character = ''
        else:
            self._character = self._source[self._read_position]

        self._position = self._read_position
        self._read_position += 1

    def _read_identifier(self) -> str:
        initial_position = self._position

        while self._is_letter(self._character) or self._is_number(self._character):
            self._read_character()

        return self._source[initial_position:self._position]

    def _read_number(self) -> str:
        initial_position = self._position

        while self._is_number(self._character):
            self._read_character()

        return self._source[initial_position:self._position]

    def _peek_character(self, skip=1) -> str:
        if self._read_position >= len(self._source):
            return ''

        return self._source[self._read_position] if skip == 1 else self._source[self._read_position + (skip - 1)]

    def _skip_whitespace(self) -> None:
        while match(r'^\s$', self._character):
            self._read_character()
