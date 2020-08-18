from dataclasses import dataclass


@dataclass
class Integer:
    value: int

    def __str__(self):
        return str(self.value)


class Number(Integer):
    value: float


class String:
    pass


class Color:
    pass


class CustomIdent:
    pass


class Ratio:
    pass


class Url:
    pass
