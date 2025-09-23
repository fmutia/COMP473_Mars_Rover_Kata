from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Protocol

@dataclass(frozen=True)
class Position:
    x: int
    y: int

class Heading(str, Enum):
    N = "N"
    E = "E"
    S = "S"
    W = "W"

class Navigator(Protocol):
    def forward(self, pos: Position, heading: Heading) -> Position: ...
    def turn_left(self, heading: Heading) -> Heading: ...
    def turn_right(self, heading: Heading) -> Heading: ...
