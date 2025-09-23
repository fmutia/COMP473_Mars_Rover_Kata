from __future__ import annotations
from typing import List
from hexrover.compat.plateau_compat import Plateau
from hexrover.compat.rover_compat import Rover

def run_simulation(input_str: str) -> str:
    # normalize and ignore blank lines
    lines: List[str] = [ln.strip() for ln in input_str.strip().splitlines() if ln.strip()]
    if not lines:
        return ""

    # plateau dims
    max_x, max_y = map(int, lines[0].split())
    plateau = Plateau(max_x, max_y)

    results: List[str] = []
    # process pairs: position line, commands line
    for i in range(1, len(lines), 2):
        x, y, heading = lines[i].split()
        rover = Rover(int(x), int(y), heading.upper(), plateau)

        commands = lines[i + 1].strip().upper()
        rover.execute_commands(commands)

        # append as "x y H" (string), matching the legacy format
        results.append(str(rover))  # uses compat __str__ -> "x y H"
        # or: x, y, h = rover.get_state(); results.append(f"{x} {y} {h}")

    return "\n".join(results)


if __name__ == "__main__":
    example_input = """5 5
    1 2 N
    LMLMLMLMM
    3 3 E
    MMRMMRMRRM"""
    print(run_simulation(example_input))