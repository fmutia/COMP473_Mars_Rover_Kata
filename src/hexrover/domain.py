from __future__ import annotations
from dataclasses import dataclass
from .ports import Position, Heading, Navigator

@dataclass(frozen=True)
class Rover:
    position: Position
    heading: Heading
    nav: Navigator

    def run(self, commands: str) -> "Rover":
        pos, head = self.position, self.heading
        for ch in commands:
            if ch == "M":
                pos = self.nav.forward(pos, head)
            elif ch == "L":
                head = self.nav.turn_left(head)
            elif ch == "R":
                head = self.nav.turn_right(head)
            else:
                continue
        return Rover(position=pos, heading=head, nav=self.nav)
