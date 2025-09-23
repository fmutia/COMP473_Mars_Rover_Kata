from __future__ import annotations
from dataclasses import dataclass
from ..adapters.grid_nav import Plateau as _Plateau

@dataclass
class Plateau:
    max_x: int
    max_y: int
    def __post_init__(self):
        self._inner = _Plateau(self.max_x, self.max_y)
    def is_within_bounds(self, x: int, y: int) -> bool:
        return self._inner.is_within_bounds(x, y)
