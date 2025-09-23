from __future__ import annotations
from ..ports import Position, Heading
from ..domain import Rover as _Rover
from ..adapters.grid_nav import GridNavigator, Plateau as _Plateau

class Rover:
    """
    Compatibility shim that looks like the legacy Rover but uses the new hex core.
    Exposes legacy-friendly methods/properties your teammate's UI expects:
      - x, y, heading (properties)
      - get_position(), get_heading(), get_state()
      - move(), move_forward() (aliases), turn_left(), turn_right()
      - execute_commands()
      - __str__ -> "x y H"
    """
    def __init__(self, x: int, y: int, heading: str, plateau: _Plateau) -> None:
        self._plat = plateau                    # compat Plateau shim wraps hex Plateau already
        self.plateau = plateau
        self._inner = _Rover(
            position=Position(x, y),
            heading=Heading[heading.upper()],
            nav=GridNavigator(self._plat._inner if hasattr(self._plat, "_inner") else self._plat),
        )

    # ---------- properties (mirror legacy attributes) ----------
    @property
    def x(self) -> int:
        return self._inner.position.x

    @property
    def y(self) -> int:
        return self._inner.position.y

    @property
    def heading(self) -> str:
        return self._inner.heading.value

    # ---------- legacy-style getters ----------
    def get_position(self) -> tuple[int, int]:
        return self.x, self.y

    def get_heading(self) -> str:
        return self.heading

    def get_state(self) -> tuple[int, int, str]:
        return self.x, self.y, self.heading

    # ---------- movement (legacy names + aliases) ----------
    def move(self) -> None:
        self._inner = self._inner.run("M")

    # Some UIs used move_forward()
    def move_forward(self) -> None:
        self.move()

    def turn_left(self) -> None:
        self._inner = self._inner.run("L")

    def left(self) -> None:
        self.turn_left()

    def turn_right(self) -> None:
        self._inner = self._inner.run("R")

    def right(self) -> None:
        self.turn_right()

    def execute_commands(self, commands: str) -> None:
        for ch in commands:
            if ch in "LRM":
                self._inner = self._inner.run(ch)

    # ---------- repr ----------
    def __str__(self) -> str:
        x, y, h = self.get_state()
        return f"{x} {y} {h}"
