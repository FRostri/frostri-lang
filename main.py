from frl.repl import start_repl
from utils.colors import TextColors

colors = TextColors()


def main() -> None:
    print(f'{colors.GREEN}Bienvenido/a a el REPL del lenguaje de programación FRostri{colors.RESET}')
    print('Escribe \'help\' para más información')

    start_repl()


if __name__ == '__main__':
    main()
