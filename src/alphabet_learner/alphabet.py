import collections
import itertools
import random
import string
import unicodedata
from getpass import getpass

from colorama import Fore, Style, init

from . import _weights
from .alphabets import ALPHABETS
from .ansi import ANSI, BAD, GOOD, RESET
from .console import console
from .get_char import GetChar
from .weights import Weights


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
            (foreign,) = random.choices(self._weights.keys, weights=weights,)
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
        try:
            for foreign, native in self._guesses():
                guess = None
                while True:
                    self._print(foreign, native, guess, (True,))
                    if guess == native:
                        break
                    guess = self._guess(foreign)
        finally:
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
