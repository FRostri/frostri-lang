from frl.repl import start_repl
from utils.colors import TextColors

colors = TextColors()


def main() -> None:
    print(f'{colors.GREEN}Welcome to the FRostri programming language REPL{colors.RESET}')
    print('Type \'help\' for mor information')

    start_repl()


if __name__ == '__main__':
    main()
