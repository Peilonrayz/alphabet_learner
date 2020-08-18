from dataclasses import dataclass

from .units import Unit


@dataclass
class Sides:
    top: Unit
    right: Unit
    bottom: Unit
    left: Unit

