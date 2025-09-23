from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Tuple
from ..ports import Position, Heading
from ..domain import Rover
from .grid_nav import Plateau, GridNavigator

@dataclass
class VisualizerController:
    max_x: int
    max_y: int
    start_x: int
    start_y: int
    start_heading: str
    _rover: Rover = field(init=False)
    _trail: List[Tuple[int,int]] = field(default_factory=list)

    def __post_init__(self):
        plat = Plateau(self.max_x, self.max_y)
        self._rover = Rover(Position(self.start_x, self.start_y), Heading[self.start_heading], GridNavigator(plat))
        self._trail.append((self.start_x, self.start_y))

    def left(self):   self._rover = self._rover.run("L")
    def right(self):  self._rover = self._rover.run("R")
    def move(self):
        before = self._rover.position
        self._rover = self._rover.run("M")
        after = self._rover.position
        if after != before: self._trail.append((after.x, after.y))

    def run(self, cmds: str):
        for ch in cmds: {"L":self.left, "R":self.right, "M":self.move}.get(ch, lambda:None)()

    def state(self) -> Tuple[int,int,str]:
        return (self._rover.position.x, self._rover.position.y, self._rover.heading.value)

    def get_trail(self) -> List[Tuple[int,int]]:
        return list(self._trail)
