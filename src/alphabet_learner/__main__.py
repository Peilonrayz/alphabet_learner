import collections
import itertools
import random
import string
import unicodedata
from getpass import getpass

from colorama import Fore, Style, init
from . import _weights
from .alphabets import ALPHABETS


init()

GOOD = Fore.CYAN + Style.BRIGHT
BAD = Fore.RED + Style.BRIGHT
RESET = Style.RESET_ALL


def iter_chunks(items, amount, fillvalue=None):
    return itertools.zip_longest(*amount * [iter(items)], fillvalue=fillvalue,)


class Weight:
    def __init__(self, weight, weights):
        self._weight = weight
        self._weights = weights
        self.correct = 0
        self.incorrect = 0

    @classmethod
    def from_dict(cls, key, items):
        return cls(
            _weights.LetterWeight(key, items[key]),
            _weights.Weights({
                _weights.LettersWeight(key, value)
                for key, value in items.items()
            })
        )
    
    @property
    def key(self):
        return self._weight.key
    
    @property
    def value(self):
        return self._weight.value

    def guess(self, guess):
        correct = self._weight.guess(guess)
        if correct:
            self.correct += 1
        else:
            self.incorrect += 1
            self._weights.guess(guess)
        return correct
    
    def update(self):
        self._weight.update()
        self._weights.update()
    
    def weight(self):
        return self._weight.weight(self._weight.key)
    
    def weights(self, ignore=None):
        return self._weight.weights(ignore=ignore)


class Weights:
    def __init__(self, alphabet):
        self._weights = _weights.Weights(
            Weight.from_dict(key, alphabet)
            for key in alphabet.keys()
        )

        self.keys = list(alphabet.keys())

    def add(self, foreign, native):
        weight = self._weights[foreign]
        if weight.guess(native):
            weight.update()

    def weights(self, previous):
        if previous is None:
            return self._weights.weights()
        return [
            (a + b) / 2
            for a, b in zip(
                self._weights.weights({previous}),
                self._weights[previous]._weights.weights({previous}),
            )
        ]
    
    def format(self, width, space=" "):
        return WeightsFormat.format(width, self._weights, space)


class WeightsFormat:
    @staticmethod
    def get_size(items):
        return max(len(str(item)) for item in items)

    @classmethod
    def get_format(cls, weights, space=" "):
        key_size = cls.get_size(weight.key or "" for weight in weights)
        correct_size = cls.get_size(weight.correct for weight in weights)
        total_size = cls.get_size(weight.correct + weight.incorrect for weight in weights)
        return (
            f"{{f_color}}{{:{space}<{key_size}}}{{reset}}"
            f" {{c_color}}{{: >{correct_size}}}{{reset}}"
            f"{{div}}{{t_color}}{{: >{total_size}}}{{reset}}",
            key_size + correct_size + total_size + 2,
        )

    @staticmethod
    def _format_chunk(format, chunk):
        for weight in chunk:
            if weight is None:
                yield ""
                continue
            foreign = weight.key
            total = weight.correct + weight.incorrect
            c_color = ""
            f_color = ""
            div = "/"
            correct = weight.correct
            if not total:
                if False:
                    foreign = ""
                    div = " "
                    correct = ""
                    total = ""
            else:
                if weight.correct >= 0.75 * total:
                    c_color = GOOD
                elif weight.correct <= 0.5 * total:
                    f_color = BAD
                    c_color = BAD
            yield format.format(
                foreign or "",
                correct,
                total,
                f_color=f_color,
                c_color=c_color,
                t_color="",
                reset=RESET,
                div=div,
            )

    @classmethod
    def format(cls, width, weights, space=" "):
        format, format_size = cls.get_format(weights, space=space)
        amount = (width + 1) // (format_size + 1)
        return "\n".join(
            " ".join(cls._format_chunk(format, chunk))
            for chunk in iter_chunks(
                (
                    weight
                    for weight in weights
                    if weight.key is not None
                ),
                amount,
            )
        )


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


class Console:
    def __init__(self):
        self.history = collections.deque(maxlen=5)

    def undo(self):
        print(
            ANSI.UP[self.history.pop().count("\n")] + "\r" + ANSI.CLEAR, end="",
        )

    def print(self, *args, sep=" ", end="\n", flush=False):
        output = sep.join(args) + end
        self.history.append(output)
        print(output, sep="", end="", flush=flush)

    def input(self, prompt=None):
        output = input(prompt)
        self.history.append((prompt or "") + output + "\n")
        return output


console = Console()


def trinary_eq(a, b):
    if a is None:
        return None
    return a == b


class Display:
    __slots__ = ("show_correct", "show_incorrect")

    def __init__(self, show_correct, show_incorrect):
        self.show_correct = show_correct
        self.show_incorrect = show_incorrect

    def movement(self, current, prev, next_line, display):
        if (
            (current is True and not self.show_correct)
            or (current is False and not self.show_incorrect)
            or (current is None and prev is None)
        ):
            display = False
            next_line = False
        return next_line, display

    def colour(self, current, prev, next_line):
        if current is None:
            if next_line or prev is None:
                return RESET
            current = prev
        if current is True:
            return GOOD
        else:
            return BAD

    def _format(self, colour, guess, next_line, display):
        yield "\n" + ANSI.UP + "\r" + ANSI.CLEAR
        guess = guess or "" if display else ""
        yield (f"{colour}{{}} -> {guess}{RESET}" + ANSI.LEFT[len(guess)])
        if next_line:
            yield "\n"

    def format(self, current, prev, guess, next_line, display, prev_next):
        next_line, display = self.movement(current, prev, next_line, display)
        colour = self.colour(current, prev, prev_next)
        return (
            "".join(self._format(colour, guess, next_line, display)),
            next_line,
        )


class Alphabet:
    __slots__ = ("_alphabet", "_weights", "_keys", "_prev", "_display", "_next_line")

    def __init__(self, alphabet, show_correct=True, show_incorrect=True):
        self._alphabet = alphabet
        self._weights = Weights(alphabet)
        self._display = Display(show_correct, show_incorrect)
        self._prev = None
        self._next_line = None

    def _guesses(self):
        previous = None
        while True:
            weights = self._weights.weights(previous)
            (foreign,) = random.choices(
                self._weights.keys, weights=weights,
            )
            if previous == foreign:
                continue
            yield foreign, self._alphabet[foreign]
            previous = foreign

    def _print(self, foreign, native, guess, next_line):
        current = trinary_eq(guess, native)
        fmt, next_line = self._display.format(
            current, self._prev, guess, current in next_line, True, self._next_line,
        )
        self._next_line = next_line
        self._prev = current
        console.print(fmt.format(foreign), end="")

    def _guess(self, foreign):
        guess = console.input("")
        console.undo()
        self._weights.add(foreign, guess)
        return guess

    def _run_multiple(self):
        foreign = None
        try:
            for foreign, native in self._guesses():
                guess = None
                while True:
                    self._print(foreign, native, guess, (True,))
                    if guess == native:
                        break
                    guess = self._guess(foreign)
        finally:
            if foreign is not None:
                console.print(f"\n\n{foreign} -> {native}")

    def _run_single(self):
        try:
            for foreign, native in self._guesses():
                guess = None
                self._print(foreign, native, guess, ())
                guess = self._guess(foreign)
                self._print(foreign, native, guess, (True, False))
        finally:
            console.print(f"\n\n{foreign} -> {native}")

    def run(self, single=False):
        try:
            if single:
                self._run_single()
            else:
                self._run_multiple()
        finally:
            console.print("\n" + self._weights.format(40))


try:
    import msvcrt
except ImportError:
    import tty, sys, termios, functools

    class GetChar:
        def __enter__(self):
            self.fd = sys.stdin.fileno()
            self.old_settings = termios.tcgetattr(self.fd)
            tty.setraw(sys.stdin.fileno())
            return functools.partial(sys.stdin.read, 1)

        def __exit__(self, _1, _2, _3):
            termios.tcsetattr(self.fd, termios.TCSADRAIN, self.old_settings)


else:
    _KEYCODES = {
        b"\x00H": ANSI.UP,
        b"\x00P": ANSI.DOWN,
    }

    def _get_char():
        char = msvcrt.getch()
        if char == b"\x00":
            char += msvcrt.getch()
        if char == b"\x03":
            raise KeyboardInterrupt()
        return _KEYCODES.get(char, char)

    class GetChar:
        def __enter__(self):
            return _get_char

        def __exit__(self, _1, _2, _3):
            pass


def menu(head, options, selection=0):
    if head:
        console.print(head)
    with GetChar() as get_char:
        while True:
            console.print(
                "\n".join(
                    GOOD + "> " + option + RESET
                    if index == selection
                    else "  " + option
                    for index, option in enumerate(options)
                )
            )
            char = get_char()
            if char == ANSI.UP:
                selection -= 1
            elif char == ANSI.DOWN:
                selection += 1
            elif char == b"\r":
                return selection
            selection %= len(options)
            console.undo()


def multi_menu(head, options, selection=0, selections=None):
    if head:
        console.print(head)
    selections = selections or set()
    with GetChar() as get_char:
        while True:
            console.print(
                "\n".join(
                    f'{GOOD}[{"x" if index in selections else " "}] {option}{RESET}'
                    if index == selection
                    else f'[{"x" if index in selections else " "}] {option}'
                    for index, option in enumerate(options)
                )
            )
            char = get_char()
            if char == ANSI.UP:
                selection -= 1
            elif char == ANSI.DOWN:
                selection += 1
            elif char == b"\r":
                if selection in selections:
                    selections.remove(selection)
                else:
                    selections.add(selection)
            elif char == b"q":
                return selections
            selection %= len(options)
            console.undo()


def get_alphabet(language):
    if language == "Greek":
        return ALPHABETS[language]
    choices = multi_menu(
        "\nReduce the alphabet",
        ["gojūon", "gojūon with dakuten", "yōon", "yōon with dakuten"],
        selections={3},
    )
    return {
        key: value
        for key, value in ALPHABETS[language].items()
        if (2 * (len(key) == 2) + bool(unicodedata.decomposition(key[0]))) in choices
    }


def select_options():
    alphabets = list(ALPHABETS.keys())
    language = alphabets[menu("Pick an alphabet", alphabets, selection=1)]
    single = not menu(
        "\nSingle or multiple chances.\n"
        "Multiple allows you to guess until you are correct. ",
        ["Single", "Multiple"],
        selection=1,
    )
    choices = multi_menu(
        "\nYou can hide previous inputs.",
        ["Hide correct entries", "Hide incorrect entries"],
        selections={0},
    )
    alphabet = get_alphabet(language)
    console.print(
        f"\nYou have selected:\n"
        f"  The {GOOD}{language}{RESET} alphabet\n"
        f'  {GOOD}{"Single" if single else "Multiple"}{RESET} chances\n'
        + (
            f"  {BAD}Hide {GOOD}correct{RESET} entries\n"
            if 0 in choices
            else f"  {GOOD}Show correct{RESET} entries\n"
        )
        + (
            f"  {BAD}Hide {GOOD}incorrect{RESET} entries\n"
            if 1 in choices
            else f"  {GOOD}Show incorrect{RESET} entries\n"
        )
    )
    return alphabet, single, 0 not in choices, 1 not in choices


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
