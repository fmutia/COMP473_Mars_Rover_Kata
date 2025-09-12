import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.plateau import Plateau
from src.rover import Rover

def test_rover_moves_correctly():
    plateau = Plateau(5, 5)
    rover = Rover(1, 2, "N", plateau)
    rover.execute_commands("LMLMLMLMM")
    assert rover.get_position() == "1 3 N"

def test_second_rover():
    plateau = Plateau(5, 5)
    rover = Rover(3, 3, "E", plateau)
    rover.execute_commands("MMRMMRMRRM")
    assert rover.get_position() == "5 1 E"
