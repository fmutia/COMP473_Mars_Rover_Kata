from __future__ import annotations
from dataclasses import dataclass
from ..ports import Navigator, Position, Heading

@dataclass(frozen=True)
class Plateau:
    max_x: int
    max_y: int
    def is_within_bounds(self, x: int, y: int) -> bool:
        return 0 <= x <= self.max_x and 0 <= y <= self.max_y

@dataclass
class GridNavigator(Navigator):
    plateau: Plateau

    ORDER = [Heading.N, Heading.E, Heading.S, Heading.W]
    DELTA = {
        Heading.N: (0, 1),
        Heading.E: (1, 0),
        Heading.S: (0, -1),
        Heading.W: (-1, 0),
    }

    def forward(self, pos: Position, heading: Heading) -> Position:
        dx, dy = self.DELTA[heading]
        nx, ny = pos.x + dx, pos.y + dy
        if self.plateau.is_within_bounds(nx, ny):
            return Position(nx, ny)
        return pos  # safe stop at edge – same policy as legacy rover

    def turn_left(self, heading: Heading) -> Heading:
        i = (self.ORDER.index(heading) - 1) % 4
        return self.ORDER[i]

    def turn_right(self, heading: Heading) -> Heading:
        i = (self.ORDER.index(heading) + 1) % 4
        return self.ORDER[i]
