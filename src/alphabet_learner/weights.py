import itertools

from . import _weights


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
            _weights.Weights(
                {_weights.LettersWeight(key, value) for key, value in items.items()}
            ),
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
            Weight.from_dict(key, alphabet) for key in alphabet.keys()
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
        total_size = cls.get_size(
            weight.correct + weight.incorrect for weight in weights
        )
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
                (weight for weight in weights if weight.key is not None), amount,
            )
        )
