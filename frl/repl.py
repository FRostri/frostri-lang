from frl.lexer import Lexer
from frl.token import (
    Token,
    TokenType
)
from utils.colors import TextColors

colors = TextColors

EOF_TOKEN: Token = Token(TokenType.EOF, '')


def start_repl() -> None:
    while (source := input(f'{colors.CYAN}>>{colors.RESET} ')) != 'salir()':
        lexer: Lexer = Lexer(source)

        if source == 'help':
            print("Esta es la ayuda")
        else:
            while (token := lexer.next_token()) != EOF_TOKEN:
                print(token)
