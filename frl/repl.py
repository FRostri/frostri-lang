from frl.lexer import Lexer
from frl.token import (
    Token,
    TokenType
)


EOF_TOKEN: Token = Token(TokenType.EOF, '')


def start_repl() -> None:
    while (source := input('>> ')) != 'salir()':
        lexer: Lexer = Lexer(source)
        
        if source == 'help':
            print("Esta es la ayuda")
        else:
            while (token := lexer.next_token()) != EOF_TOKEN:
                print(token)
