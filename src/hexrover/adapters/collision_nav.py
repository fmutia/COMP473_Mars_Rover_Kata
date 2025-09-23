from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Set
from ..ports import Navigator, Position, Heading

@dataclass
class Occupancy:
    positions: Dict[str, Position]

    def occupied_except(self, self_id: str) -> Set[Position]:
        return {pos for rid, pos in self.positions.items() if rid != self_id}

@dataclass
class CollisionNavigator(Navigator):
    inner: Navigator
    occ: Occupancy
    self_id: str

    def forward(self, pos: Position, heading: Heading) -> Position:
        nxt = self.inner.forward(pos, heading)
        if nxt == pos: return pos
        if nxt in self.occ.occupied_except(self_id=self.self_id): return pos
        return nxt

    def turn_left(self, heading: Heading) -> Heading:  return self.inner.turn_left(heading)
    def turn_right(self, heading: Heading) -> Heading: return self.inner.turn_right(heading)
