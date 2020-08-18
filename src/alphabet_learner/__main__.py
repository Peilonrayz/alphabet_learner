from colorama import init

from .alphabet import Alphabet
from .menu import select_options
from boxes.datatypes import Unit, UnitTypes, Calc

init()


def main():
    try:
        alphabet, single, correct, incorrect = select_options()
        Alphabet(alphabet, show_correct=correct, show_incorrect=incorrect,).run(
            single=single
        )
    except KeyboardInterrupt:
        pass


def disp(unit):
    print(unit, repr(unit))


def main():
    disp(Unit.build(0))
    disp(Unit.build(20, 'px'))
    disp(Unit.build(1, '%', UnitTypes.ANGLE))
    disp(Calc.build(1))
    disp(Calc.build([1, Unit.build(20, 'px')], ['+']))


if __name__ == "__main__":
    main()
