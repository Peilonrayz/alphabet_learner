import collections
import itertools

flatten = itertools.chain.from_iterable


class Weight:
    def __init__(self, key, value, guesses=None, history=10):
        self.key = key
        self.value = value
        self._guesses = collections.deque(guesses or [], history)
        self._guess = 0

    def guess(self, guess):
        self._guess += 1
        return guess == self.value

    def update(self):
        if self._guess:
            self._guesses.append(self._guess)

    def _weight(self):
        raise NotImplementedError("Weight.weight is not implemented")

    def weight(self, key):
        if key == self.key:
            self._weight(key)
        raise ValueError(f"No weight {weight}")

    def weights(self, ignore=None):
        return [self._weight()]


class LetterWeight(Weight):
    def _weight(self):
        correct = len(self._guesses)
        incorrect = sum(self._guesses) - correct
        return max(1, incorrect - correct + 1) * min(5, max(1, 5 - correct))


class LettersWeight(Weight):
    def _weight(self):
        correct = len(self._guesses)
        incorrect = sum(self._guesses)
        return max(1, incorrect - correct + 1)


class Weights:
    def __init__(self, weights):
        self._weights = {w.key: w for w in weights}
        by_value = {}
        for weight in weights:
            by_value.setdefault(weight.value, []).append(weight.key)
        self._by_value = by_value

    def __getitem__(self, key):
        return self._weights[key]

    def __iter__(self):
        return iter(self._weights.values())

    def guess(self, guess):
        return any(
            self._weights[key].guess(guess) for key in self._by_value.get(guess, [])
        )

    def update(self):
        for weight in self._weights.values():
            weight.update()

    def weight(self, key):
        return self._weights[key].weight(key)

    def weights(self, ignore=None):
        ignore = set(ignore or [])
        return list(
            flatten(
                [
                    weight.weights() if key not in ignore else [0]
                    for key, weight in self._weights.items()
                ]
            )
        )
