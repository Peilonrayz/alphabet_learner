import string

from colorama import Fore, Style, init

GOOD = Fore.CYAN + Style.BRIGHT
BAD = Fore.RED + Style.BRIGHT
RESET = Style.RESET_ALL


class StrCode:
    __slots__ = ("fmt", "args")
    FORMATTER = string.Formatter()

    def __init__(self, fmt, args=None):
        self.fmt = fmt
        self.args = args or ()

    def __str__(self):
        return self.fmt.format(";".join(self.args))

    def __getitem__(self, args):
        if not isinstance(args, tuple):
            args = (args,)
        return StrCode(self.fmt, self.args + tuple(map(str, args)))

    def __add__(self, other):
        return str(self) + other

    def __radd__(self, other):
        return other + str(self)


class ANSI:
    POSITION = StrCode("\033[{}H")
    POSITION_ALT = StrCode("\033[{}f")
    UP = StrCode("\033[{}A")
    DOWN = StrCode("\033[{}B")
    RIGHT = StrCode("\033[{}C")
    LEFT = StrCode("\033[{}D")
    CLEAR = StrCode("\033[{}J")
    CLEAR_LINE = StrCode("\033[{}K")
