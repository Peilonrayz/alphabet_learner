import enum
from dataclasses import dataclass
from typing import Optional, ClassVar, Dict


class UnitTypes(enum.Enum):
    NONE = 0
    FLEX = enum.auto()
    ANGLE = enum.auto()
    FREQUENCY = enum.auto()
    LENGTH = enum.auto()
    RESOLUTION = enum.auto()
    TIME = enum.auto()


@dataclass
class Unit:
    value: float
    UNIT: ClassVar[Optional[str]] = None
    UNITS: ClassVar[Dict[str, "Unit"]] = {}
    TYPE: ClassVar[UnitTypes] = UnitTypes.NONE

    def __init_subclass__(cls, /, unit: Optional[str], type=None, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.UNIT = unit
        cls.UNITS = {}
        cls.TYPE = type = _get_type(cls) if type is None else type
        if unit is None:
            return
        cls2 = Unit.UNITS.get(unit)
        if cls2 is not None:
            raise ValueError("Multiple classes with unit {unit} - {cls} and {cls2}")
        for c in cls.__mro__[1:-1]:
            c.UNITS[(unit, type)] = cls
    
    @classmethod
    def build(cls, value: float, unit: Optional[str] = None, type: Optional[UnitTypes]=None):
        if unit is None:
            if value == 0:
                return ZERO
            else:
                raise ValueError(f"Unit must be specified with non-zero value")
        classes = _get_classes(
            cls.UNITS,
            unit,
            list(UnitTypes) if type is None else [type],
        )
        if len(classes) == 0:
            if type is None:
                raise ValueError(f"Unknown unit {unit!r}")
            else:
                raise ValueError(f"Unknown unit {unit!r} with type {type}")
        if len(classes) != 1:
            raise ValueError(f"Ambiguous unit {unit!r} please specify a type")
        return classes[0](value)

    def __str__(self):
        return f"{self.value}{'' if self.UNIT is None else self.UNIT}"


ZERO = Unit(0)


def _get_type(cls):
    for _cls in cls.__mro__[1:-1]:
        if _cls.TYPE is not UnitTypes.NONE:
            return _cls.TYPE
    return UnitTypes.NONE


def _get_classes(units, unit, UnitTypes):
    classes = []
    for type in UnitTypes:
        cls = units.get((unit, type))
        if cls is not None:
            classes.append(cls)
    return classes


class Dimension(Unit, unit=None):
    pass


class Flex(Dimension, unit='fr', type=UnitTypes.FLEX):
    pass


class Angle(Dimension, unit=None, type=UnitTypes.ANGLE):
    pass


class AngleDegree(Angle, unit='deg'):
    pass


class AngleRadian(Angle, unit='rad'):
    pass


class AngleGradian(Angle, unit='grad'):
    pass


class AngleTurn(Angle, unit='turn'):
    pass


class Frequency(Dimension, unit=None, type=UnitTypes.FREQUENCY):
    pass


class FrequencyHertz(Frequency, unit='Hz'):
    pass


class FrequencyKiloHertz(Frequency, unit='KhZ'):
    pass


class Length(Dimension, unit=None, type=UnitTypes.LENGTH):
    pass


class LengthCap(Length, unit='cap'):
    pass


class LengthCh(Length, unit='ch'):
    pass


class LengthEm(Length, unit='em'):
    pass


class LengthEx(Length, unit='ex'):
    pass


class LengthIc(Length, unit='ic'):
    pass


class LengthLineHeight(Length, unit='lh'):
    pass


class LengthRootEm(Length, unit='rem'):
    pass


class LengthRootLineHeight(Length, unit='rlh'):
    pass


class LengthViewportHeight(Length, unit='vh'):
    pass


class LengthViewportWidth(Length, unit='vw'):
    pass


class LengthRootInline(Length, unit='vi'):
    pass


class LengthRootBlock(Length, unit='vb'):
    pass


class LengthViewportMin(Length, unit='vmin'):
    pass


class LengthViewportMax(Length, unit='vmax'):
    pass


class LengthPixel(Length, unit='px'):
    pass


class LengthCentiMeter(Length, unit='cm'):
    pass


class LengthMilliMeter(Length, unit='mm'):
    pass


class LengthQ(Length, unit='Q'):
    pass


class LengthInch(Length, unit='in'):
    pass


class LengthPica(Length, unit='pc'):
    pass


class LengthPoint(Length, unit='pt'):
    pass


class Resolution(Dimension, unit=None, type=UnitTypes.RESOLUTION):
    pass


class ResolutionInch(Resolution, unit='dpi'):
    pass


class ResolutionCentiMeter(Resolution, unit='dpcm'):
    pass


class ResolutionPixel(Resolution, unit='dppx'):
    pass


class Time(Dimension, unit=None, type=UnitTypes.TIME):
    pass


class TimeSeconds(Time, unit='s'):
    pass


class TimeMilliSeconds(Time, unit='ms'):
    pass


class Percentage(Unit, unit=None):
    pass


class PercentageAngle(Percentage, unit='%', type=UnitTypes.ANGLE):
    pass


class PercentageFrequency(Percentage, unit='%', type=UnitTypes.FREQUENCY):
    pass


class PercentageLength(Percentage, unit='%', type=UnitTypes.LENGTH):
    pass


class PercentageTime(Percentage, unit='%', type=UnitTypes.TIME):
    pass
