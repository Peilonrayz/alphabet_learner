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
