import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from hexrover.compat.plateau_compat import Plateau
from hexrover.compat.rover_compat import Rover

def test_rover_moves_correctly():
    plateau = Plateau(5, 5)
    rover = Rover(1, 2, "N", plateau)
    rover.execute_commands("LMLMLMLMM")
    assert str(rover) == "1 3 N"

def test_second_rover():
    plateau = Plateau(5, 5)
    rover = Rover(3, 3, "E", plateau)
    rover.execute_commands("MMRMMRMRRM")
    assert str(rover) == "5 1 E"
