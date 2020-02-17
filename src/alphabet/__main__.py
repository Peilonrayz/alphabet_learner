import random
import string
import collections
import unicodedata
import itertools
from getpass import getpass

from colorama import init, Fore, Style

init()

ALPHABETS = {
    'Greek': {
        'α': 'alpha',
        'Α': 'Alpha',
        'β': 'beta',
        'Β': 'Beta',
        'γ': 'gamma',
        'Γ': 'Gamma',
        'δ': 'delta',
        'Δ': 'Delta',
        'ε': 'epsilon',
        'Ε': 'Epsilon',
        'ζ': 'zeta',
        'Ζ': 'Zeta',
        'η': 'eta',
        'Η': 'Eta',
        'θ': 'theta',
        'Θ': 'Theta',
        'ι': 'iota',
        'Ι': 'Iota',
        'κ': 'kappa',
        'Κ': 'Kappa',
        'λ': 'lambda',
        'Λ': 'Lambda',
        'μ': 'mu',
        'Μ': 'Mu',
        'ν': 'nu',
        'Ν': 'Nu',
        'ξ': 'xi',
        'Ξ': 'Xi',
        'ο': 'omicron',
        'Ο': 'Omicron',
        'π': 'pi',
        'Π': 'Pi',
        'ρ': 'rho',
        'Ρ': 'Rho',
        'σ': 'sigma',
        'Σ': 'Sigma',
        'ς': 'sigma',
        'τ': 'tau',
        'Τ': 'Tau',
        'υ': 'upsilon',
        'Υ': 'Upsilon',
        'φ': 'phi',
        'Φ': 'Phi',
        'χ': 'chi',
        'Χ': 'Chi',
        'ψ': 'psi',
        'Ψ': 'Psi',
        'ω': 'omega',
        'Ω': 'Omega',
    },
    'Hiragana': {
        'ん': 'n',
        'あ': 'a',
        'か': 'ka',
        'さ': 'sa',
        'た': 'ta',
        'な': 'na',
        'は': 'ha',
        'ま': 'ma',
        'や': 'ya',
        'ら': 'ra',
        'わ': 'wa',
        'が': 'ga',
        'ざ': 'za',
        'だ': 'da',
        'ば': 'ba',
        'ぱ': 'pa',
        'きゃ': 'kya',
        'しゃ': 'sha',
        'ちゃ': 'cha',
        'にゃ': 'nya',
        'ひゃ': 'hya',
        'みゃ': 'mya',
        'りゃ': 'rya',
        'ぎゃ': 'gya',
        'じゃ': 'ja',
        'ぢゃ': 'ja',
        'びゃ': 'bya',
        'ぴゃ': 'pya',
        'い': 'i',
        'き': 'ki',
        'し': 'shi',
        'ち': 'chi',
        'に': 'ni',
        'ひ': 'hi',
        'み': 'mi',
        'り': 'ri',
        'ぎ': 'gi',
        'じ': 'ji',
        'ぢ': 'ji',
        'び': 'bi',
        'ぴ': 'pi',
        'う': 'u',
        'く': 'ku',
        'す': 'su',
        'つ': 'tsu',
        'ぬ': 'nu',
        'ふ': 'fu',
        'む': 'mu',
        'ゆ': 'yu',
        'る': 'ru',
        'ぐ': 'gu',
        'ず': 'zu',
        'づ': 'dzu',
        'ぶ': 'bu',
        'ぷ': 'pu',
        'きゅ': 'kyu',
        'しゅ': 'shu',
        'ちゅ': 'chu',
        'にゅ': 'nyu',
        'ひゅ': 'hyu',
        'みゅ': 'myu',
        'りゅ': 'ryu',
        'ぎゅ': 'gyu',
        'じゅ': 'ju',
        'ぢゅ': 'ju',
        'びゅ': 'byu',
        'ぴゅ': 'pyu',
        'え': 'e',
        'け': 'ke',
        'せ': 'se',
        'て': 'te',
        'ね': 'ne',
        'へ': 'he',
        'め': 'me',
        'れ': 're',
        'げ': 'ge',
        'ぜ': 'ze',
        'で': 'de',
        'べ': 'be',
        'ぺ': 'pe',
        'お': 'o',
        'こ': 'ko',
        'そ': 'so',
        'と': 'to',
        'の': 'no',
        'ほ': 'ho',
        'も': 'mo',
        'よ': 'yo',
        'ろ': 'ro',
        'を': 'wo',
        'ご': 'go',
        'ぞ': 'zo',
        'ど': 'do',
        'ぼ': 'bo',
        'ぽ': 'po',
        'きょ': 'kyo',
        'しょ': 'sho',
        'ちょ': 'cho',
        'にょ': 'nyo',
        'ひょ': 'hyo',
        'みょ': 'myo',
        'りょ': 'ryo',
        'ぎょ': 'gyo',
        'じょ': 'jo',
        'ぢょ': 'jo',
        'びょ': 'byo',
        'ぴょ': 'pyo',
    },
    'Katakana': {
        'ン': 'n',
        'ア': 'a',
        'カ': 'ka',
        'サ': 'sa',
        'タ': 'ta',
        'ナ': 'na',
        'ハ': 'ha',
        'マ': 'ma',
        'ヤ': 'ya',
        'ラ': 'ra',
        'ワ': 'wa',
        'ガ': 'ga',
        'ザ': 'za',
        'ダ': 'da',
        'バ': 'ba',
        'パ': 'pa',
        'キャ': 'kya',
        'シャ': 'sha',
        'チャ': 'cha',
        'ニャ': 'nya',
        'ヒャ': 'hya',
        'ミャ': 'mya',
        'リャ': 'rya',
        'ギャ': 'gya',
        'ジャ': 'ja',
        'ヂャ': 'ja',
        'ビャ': 'bya',
        'ピャ': 'pya',

        'イ': 'i',
        'キ': 'ki',
        'シ': 'shi',
        'チ': 'chi',
        'ニ': 'ni',
        'ヒ': 'hi',
        'ミ': 'mi',
        'リ': 'ri',
        'ギ': 'gi',
        'ジ': 'ji',
        'ヂ': 'ji',
        'ビ': 'bi',
        'ピ': 'pi',

        'ウ': 'u',
        'ク': 'ku',
        'ス': 'su',
        'ツ': 'tsu',
        'ヌ': 'nu',
        'フ': 'fu',
        'ム': 'mu',
        'ユ': 'yu',
        'ル': 'ru',
        'グ': 'gu',
        'ズ': 'zu',
        'ヅ': 'zu',
        'ブ': 'bu',
        'プ': 'pu',
        'キュ': 'kyu',
        'シュ': 'shu',
        'チュ': 'chu',
        'ニュ': 'nyu',
        'ヒュ': 'hyu',
        'ミュ': 'myu',
        'リュ': 'ryu',
        'ギュ': 'gyu',
        'ジュ': 'ju',
        'ヂュ': 'ju',
        'ビュ': 'byu',
        'ピュ': 'pyu',

        'エ': 'e',
        'ケ': 'ke',
        'セ': 'se',
        'テ': 'te',
        'ネ': 'ne',
        'ヘ': 'he',
        'メ': 'me',
        'レ': 're',
        'ゲ': 'ge',
        'ゼ': 'ze',
        'デ': 'de',
        'ベ': 'be',
        'ペ': 'pe',

        'オ': 'o',
        'コ': 'ko',
        'ソ': 'so',
        'ト': 'to',
        'ノ': 'no',
        'ホ': 'ho',
        'モ': 'mo',
        'ヨ': 'yo',
        'ロ': 'ro',
        'ヲ': 'wo',
        'ゴ': 'go',
        'ゾ': 'zo',
        'ド': 'do',
        'ボ': 'bo',
        'ポ': 'po',
        'キョ': 'kyo',
        'ショ': 'sho',
        'チョ': 'cho',
        'ニョ': 'nyo',
        'ヒョ': 'hyo',
        'ミョ': 'myo',
        'リョ': 'ryo',
        'ギョ': 'gyo',
        'ジョ': 'jo',
        'ヂョ': 'jo',
        'ビョ': 'byo',
        'ピョ': 'pyo',
    }
}

GOOD = Fore.CYAN + Style.BRIGHT
BAD = Fore.RED + Style.BRIGHT
RESET = Style.RESET_ALL


def weight(incorrect, correct):
    return max(1, incorrect - correct)


def weights(weights):
    total = sum(weights) or 1
    return [
        weight / total
        for weight in weights
    ]


class Weight:
    def __init__(self, keys):
        self.correct = 0
        self.incorrect = 0
        self.native = {
            foreign: 0
            for foreign in keys
        }

    def weight(self):
        return weight(self.incorrect, self.correct)
    
    def weights(self, keys):
        return weights([
            weight(self.native[key], self.correct)
            for key in keys
        ])


def iter_chunks(items, amount, fillvalue=None):
    return itertools.zip_longest(
        *amount*[iter(items)],
        fillvalue=fillvalue,
    )


class Weights:
    def __init__(self, alphabet):
        self.keys = list(alphabet.keys())
        natives = {}
        for foreign, native in alphabet.items():
            natives.setdefault(native, set()).add(foreign)
        self._native = natives
        self._weights = {
            foreign: Weight(self.keys)
            for foreign in self.keys
        }
        self._weights[None] = Weight(self.keys)

    def add(self, foreign, native):
        weight = self._weights[foreign]
        other_foreign = self._native.get(native, set())
        if foreign in other_foreign:
            weight.correct += 1
        else:
            weight.incorrect += 1
            for other in other_foreign:
                weight.native[other] += 1

    def _gen_weights(self, previous, keys):
        return weights([
            0
            if key == previous else
            self._weights[key].weight()
            for key in keys
        ])

    def weights(self, previous):
        return [
            (a + b) / 2
            for a, b in zip(
                self._gen_weights(previous, self.keys),
                self._weights[previous].weights(self.keys),
            )
        ]
    
    def get_format(self):
        foreign_size = max(
            len(foreign or '')
            for foreign in self._weights
        )
        correct_size = max(
            len(str(weight.correct))
            for weight in self._weights.values()
        )
        total_size = max(
            len(str(weight.correct + weight.incorrect))
            for weight in self._weights.values()
        )
        return (
            f'{{f_color}}{{:　<{foreign_size}}}{{reset}}'
            f' {{c_color}}{{: >{correct_size}}}{{reset}}'
            f'{{div}}{{t_color}}{{: >{total_size}}}{{reset}}',
            foreign_size + correct_size + total_size + 2,
        )

    def _format_chunk(self, format, chunk):
        for value in chunk:
            if value is None:
                yield ''
                continue
            foreign, weight = value
            total = weight.correct + weight.incorrect
            c_color = ''
            f_color = ''
            div = '/'
            correct = weight.correct
            if not total:
                if False:
                    foreign = ''
                    div = ' '
                    correct = ''
                    total = ''
            else:
                if weight.correct >= 0.75 * total:
                    c_color = GOOD
                elif weight.correct <= 0.5 * total:
                    f_color = BAD
                    c_color = BAD
            yield format.format(
                foreign or '',
                correct,
                total,
                f_color=f_color,
                c_color=c_color,
                t_color='',
                reset=RESET,
                div=div,
            )
    
    def format(self, width):
        format, format_size = self.get_format()
        amount = (
            (width + 1)
            // (format_size + 1)
        )
        return '\n'.join(
            ' '.join(self._format_chunk(format, chunk))
            for chunk in iter_chunks(
                (
                    (foreign, weight)
                    for foreign, weight in self._weights.items()
                    if foreign is not None
                ),
                amount,
            )
        )


class StrCode:
    __slots__ = ('fmt', 'args')
    FORMATTER = string.Formatter()

    def __init__(self, fmt, args=None):
        self.fmt = fmt
        self.args = args or ()
    
    def __str__(self):
        return self.fmt.format(';'.join(self.args))
    
    def __getitem__(self, args):
        if not isinstance(args, tuple):
            args = (args,)
        return StrCode(self.fmt, self.args + tuple(map(str, args)))
    
    def __add__(self, other):
        return str(self) + other
    
    def __radd__(self, other):
        return other + str(self)


class ANSI:
    POSITION = StrCode('\033[{}H')
    POSITION_ALT = StrCode('\033[{}f')
    UP = StrCode('\033[{}A')
    DOWN = StrCode('\033[{}B')
    RIGHT = StrCode('\033[{}C')
    LEFT = StrCode('\033[{}D')
    CLEAR = StrCode('\033[{}J')
    CLEAR_LINE = StrCode('\033[{}K')


class Console:
    def __init__(self):
        self.history = collections.deque(maxlen=5)
    
    def undo(self):
        print(
            ANSI.UP[self.history.pop().count('\n')] + '\r' + ANSI.CLEAR,
            end='',
        )

    def print(self, *args, sep=' ', end='\n', flush=False):
        output = sep.join(args) + end
        self.history.append(output)
        print(output, sep='', end='', flush=flush)

    def input(self, prompt=None):
        output = input(prompt)
        self.history.append((prompt or '') + output + '\n')
        return output


console = Console()


def trinary_eq(a, b):
    if a is None:
        return None
    return a == b


class Display:
    __slots__ = ('show_correct', 'show_incorrect')

    def __init__(self, show_correct, show_incorrect):
        self.show_correct = show_correct
        self.show_incorrect = show_incorrect

    def movement(self, current, prev, next_line, display):
        if ((current is True and not self.show_correct)
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
        yield '\n' + ANSI.UP + '\r' + ANSI.CLEAR
        guess = guess or '' if display else ''
        yield (
            f'{colour}{{}} -> {guess}{RESET}'
            + ANSI.LEFT[len(guess)]
        )
        if next_line:
            yield '\n'

    def format(self, current, prev, guess, next_line, display, prev_next):
        next_line, display = self.movement(current, prev, next_line, display)
        colour = self.colour(current, prev, prev_next)
        return (
            ''.join(self._format(colour, guess, next_line, display)),
            next_line,
        )


class Alphabet:
    __slots__ = (
        '_alphabet', '_weights', '_keys', '_prev', '_display', '_next_line'
    )

    def __init__(self, alphabet, show_correct=True, show_incorrect=True):
        self._alphabet = alphabet
        self._weights = Weights(alphabet)
        self._display = Display(show_correct, show_incorrect)
        self._prev = None
        self._next_line = None

    def _guesses(self):
        previous = None
        while True:
            foreign, = random.choices(
                self._weights.keys,
                weights=self._weights.weights(previous),
            )
            if previous == foreign:
                continue
            yield foreign, self._alphabet[foreign]
            previous = foreign

    def _print(self, foreign, native, guess, next_line):
        current = trinary_eq(guess, native)
        fmt, next_line = self._display.format(
            current,
            self._prev,
            guess,
            current in next_line,
            True,
            self._next_line,
        )
        self._next_line = next_line
        self._prev = current
        console.print(fmt.format(foreign), end='')
    
    def _guess(self, foreign):
        guess = console.input('')
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
            console.print(f'\n\n{foreign} -> {native}')

    def _run_single(self):
        try:
            for foreign, native in self._guesses():
                guess = None
                self._print(foreign, native, guess, ())
                guess = self._guess(foreign)
                self._print(foreign, native, guess, (True, False))
        finally:
            console.print(f'\n\n{foreign} -> {native}')

    def run(self, single=False):
        try:
            if single:
                self._run_single()
            else:
                self._run_multiple()
        finally:
            console.print('\n' + self._weights.format(40))

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
        b'\x00H': ANSI.UP,
        b'\x00P': ANSI.DOWN,
    }

    def _get_char():
        char = msvcrt.getch()
        if char == b'\x00':
            char += msvcrt.getch()
        if char == b'\x03':
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
            console.print('\n'.join(
                GOOD + '> ' + option + RESET
                if index == selection else
                '  ' + option
                for index, option in enumerate(options)
            ))
            char = get_char()
            if char == ANSI.UP:
                selection -= 1
            elif char == ANSI.DOWN:
                selection += 1
            elif char == b'\r':
                return selection
            selection %= len(options)
            console.undo()


def multi_menu(head, options, selection=0, selections=None):
    if head:
        console.print(head)
    selections = selections or set()
    with GetChar() as get_char:
        while True:
            console.print('\n'.join(
                f'{GOOD}[{"x" if index in selections else " "}] {option}{RESET}'
                if index == selection else
                f'[{"x" if index in selections else " "}] {option}'
                for index, option in enumerate(options)
            ))
            char = get_char()
            if char == ANSI.UP:
                selection -= 1
            elif char == ANSI.DOWN:
                selection += 1
            elif char == b'\r':
                if selection in selections:
                    selections.remove(selection)
                else:
                    selections.add(selection)
            elif char == b'q':
                return selections
            selection %= len(options)
            console.undo()


def get_alphabet(language):
    if language == 'Greek':
        return ALPHABETS[language]
    choices = multi_menu(
        '\nReduce the alphabet',
        [
            'gojūon',
            'gojūon with dakuten',
            'yōon',
            'yōon with dakuten'
        ],
        selections={3},
    )
    return {
        key: value
        for key, value in ALPHABETS[language].items()
        if (
            2*(len(key) == 2)
            + bool(unicodedata.decomposition(key[0]))
        ) in choices
    }



def select_options():
    alphabets = list(ALPHABETS.keys())
    language = alphabets[menu('Pick an alphabet', alphabets, selection=1)]
    single = not menu(
        '\nSingle or multiple chances.\n'
        'Multiple allows you to guess until you are correct. ',
        ['Single', 'Multiple'],
        selection=1,
    )
    choices = multi_menu(
        '\nYou can hide previous inputs.',
        ['Hide correct entries', 'Hide incorrect entries'],
        selections={0},
    )
    alphabet = get_alphabet(language)
    console.print(
        f'\nYou have selected:\n'
        f'  The {GOOD}{language}{RESET} alphabet\n'
        f'  {GOOD}{"Single" if single else "Multiple"}{RESET} chances\n'
        + (
            f'  {BAD}Hide {GOOD}correct{RESET} entries\n'
            if 0 in choices else
            f'  {GOOD}Show correct{RESET} entries\n'
        )
        + (
            f'  {BAD}Hide {GOOD}incorrect{RESET} entries\n'
            if 1 in choices else
            f'  {GOOD}Show incorrect{RESET} entries\n'
        )
    )
    return alphabet, single, 0 not in choices, 1 not in choices


def main():
    alphabet, single, correct, incorrect = select_options()
    Alphabet(
        alphabet,
        show_correct=correct,
        show_incorrect=incorrect,
    ).run(single=single)



if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
