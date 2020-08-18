import collections.abc
from typing import Union, Sequence, Optional

from .primitives import Number
from .units import Unit, UnitTypes


_Value = Union[Unit, Number, float, int]


class Calc:
    type: UnitTypes

    @classmethod
    def build(
        cls,
        values: Union[_Value, Sequence[_Value]],
        operators: Sequence[str] = [],
    ):
        _values: Sequence[_Value] = (
            values
            if isinstance(values, collections.abc.Sequence) else
            [values]
        )
        if len(_values) != len(operators) + 1:
            raise ValueError("There must be one less operator than values.")
        calc = CalcOperators(
            [
                CalcValue(value)
                if not isinstance(value, (float, int)) else
                CalcValue(Number(value))
                for value in _values
            ],
            operators[:],
        )
        if len(operators) == 0:
            return calc._values[0]
        return calc


class CalcValue(Calc):
    _value: Union[Unit, Number]

    def __init__(self, value: Union[Unit, Number]):
        self._value = value
        if isinstance(value, Unit):
            self.type = value.TYPE
        else:
            self.type = UnitTypes.NONE
    
    def __str__(self):
        return str(self._value)
    
    def __repr__(self):
        return f"CalcValue({self._value!r})"


class CalcOperators(Calc):
    _values: Sequence[Calc]
    _operators: Sequence[str]

    def __init__(self, values: Sequence[Calc], operators: Sequence[str]):
        if len(values) != len(operators) + 1:
            raise ValueError("There must be one less operator than values.")
        types = {value.type for value in values if value.type is not UnitTypes.NONE}
        if 1 < len(types):
            raise ValueError(f"Cannot mix types {types}")
        self._values = values
        self._operators = operators
    
    def __str__(self):
        values = [None] * (len(self._values) * 2 - 1)
        values[0::2] = self._values
        values[1::2] = self._operators
        return " ".join(str(v) for v in values)
    
    def __repr__(self):
        return f"CalcOperators({self._values!r}, {self._operators!r})"
