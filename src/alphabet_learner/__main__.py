from colorama import init

from .alphabet import Alphabet
from .menu import select_options

init()


def main():
    try:
        alphabet, single, correct, incorrect = select_options()
        Alphabet(alphabet, show_correct=correct, show_incorrect=incorrect,).run(
            single=single
        )
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
