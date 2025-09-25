import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from hexrover.compat.plateau_compat import Plateau
from hexrover.compat.rover_compat import Rover

def test_classic_examples():
    """
    Ensure the legacy-compatible shims + adapters reproduce the classic kata examples.
    - Rover 1: start 1 2 N -> LMLMLMLMM -> 1 3 N
    - Rover 2: start 3 3 E -> MMRMMRMRRM -> 5 1 E
    """
    plateau = Plateau(5, 5)

    rover1 = Rover(1, 2, "N", plateau)
    rover1.execute_commands("LMLMLMLMM")
    assert str(rover1) == "1 3 N"

    rover2 = Rover(3, 3, "E", plateau)
    rover2.execute_commands("MMRMMRMRRM")
    assert str(rover2) == "5 1 E"


def test_legacy_aliases_and_getters():
    """
    Basic legacy API coverage so the UI-level code gets the values it expects.
    """
    plateau = Plateau(5, 5)
    rover = Rover(0, 0, "E", plateau)

    # move_forward alias
    rover.move_forward()
    assert rover.get_position()[0] == 1

    # left alias
    rover.left()
    assert rover.get_heading() == "N"

    # getters and string repr
    assert rover.get_state() == (1, 0, "N")
    assert str(rover).startswith("1 0")