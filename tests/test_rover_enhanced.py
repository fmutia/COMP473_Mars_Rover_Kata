import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.plateau import Plateau
from src.rover import Rover
import pytest


class TestRoverCreation:
    """Test rover initialization"""

    def test_rover_creation(self):
        plateau = Plateau(5, 5)
        rover = Rover(1, 2, "N", plateau)
        assert rover.x == 1
        assert rover.y == 2
        assert rover.heading == "N"
        assert rover.plateau == plateau

    def test_rover_all_directions(self):
        plateau = Plateau(5, 5)
        directions = ["N", "E", "S", "W"]
        for direction in directions:
            rover = Rover(2, 2, direction, plateau)
            assert rover.heading == direction


class TestRoverRotation:
    """Test rover turning functionality"""

    def test_turn_right_full_cycle(self):
        plateau = Plateau(5, 5)
        rover = Rover(2, 2, "N", plateau)

        rover.turn_right()
        assert rover.heading == "E"

        rover.turn_right()
        assert rover.heading == "S"

        rover.turn_right()
        assert rover.heading == "W"

        rover.turn_right()
        assert rover.heading == "N"  # Back to start

    def test_turn_left_full_cycle(self):
        plateau = Plateau(5, 5)
        rover = Rover(2, 2, "N", plateau)

        rover.turn_left()
        assert rover.heading == "W"

        rover.turn_left()
        assert rover.heading == "S"

        rover.turn_left()
        assert rover.heading == "E"

        rover.turn_left()
        assert rover.heading == "N"  # Back to start

    def test_multiple_rotations(self):
        plateau = Plateau(5, 5)
        rover = Rover(2, 2, "N", plateau)

        # Multiple right turns
        for _ in range(8):  # Two full cycles
            rover.turn_right()
        assert rover.heading == "N"

        # Multiple left turns
        for _ in range(12):  # Three full cycles
            rover.turn_left()
        assert rover.heading == "N"


class TestRoverMovement:
    """Test rover movement in all directions"""

    def test_move_north(self):
        plateau = Plateau(5, 5)
        rover = Rover(2, 2, "N", plateau)
        rover.move()
        assert rover.x == 2
        assert rover.y == 3

    def test_move_east(self):
        plateau = Plateau(5, 5)
        rover = Rover(2, 2, "E", plateau)
        rover.move()
        assert rover.x == 3
        assert rover.y == 2

    def test_move_south(self):
        plateau = Plateau(5, 5)
        rover = Rover(2, 2, "S", plateau)
        rover.move()
        assert rover.x == 2
        assert rover.y == 1

    def test_move_west(self):
        plateau = Plateau(5, 5)
        rover = Rover(2, 2, "W", plateau)
        rover.move()
        assert rover.x == 1
        assert rover.y == 2


class TestRoverBoundaries:
    """Test rover boundary collision detection"""

    def test_cannot_move_beyond_north_boundary(self):
        plateau = Plateau(5, 5)
        rover = Rover(2, 5, "N", plateau)
        rover.move()  # Try to move north from top edge
        assert rover.x == 2
        assert rover.y == 5  # Should not move

    def test_cannot_move_beyond_east_boundary(self):
        plateau = Plateau(5, 5)
        rover = Rover(5, 2, "E", plateau)
        rover.move()  # Try to move east from right edge
        assert rover.x == 5  # Should not move
        assert rover.y == 2

    def test_cannot_move_beyond_south_boundary(self):
        plateau = Plateau(5, 5)
        rover = Rover(2, 0, "S", plateau)
        rover.move()  # Try to move south from bottom edge
        assert rover.x == 2
        assert rover.y == 0  # Should not move

    def test_cannot_move_beyond_west_boundary(self):
        plateau = Plateau(5, 5)
        rover = Rover(0, 2, "W", plateau)
        rover.move()  # Try to move west from left edge
        assert rover.x == 0  # Should not move
        assert rover.y == 2


class TestRoverCommands:
    """Test rover command processing"""

    def test_empty_commands(self):
        plateau = Plateau(5, 5)
        rover = Rover(2, 2, "N", plateau)
        initial_position = rover.get_position()
        rover.execute_commands("")
        assert rover.get_position() == initial_position

    def test_single_commands(self):
        plateau = Plateau(5, 5)

        # Test single L
        rover = Rover(2, 2, "N", plateau)
        rover.execute_commands("L")
        assert rover.heading == "W"

        # Test single R
        rover = Rover(2, 2, "N", plateau)
        rover.execute_commands("R")
        assert rover.heading == "E"

        # Test single M
        rover = Rover(2, 2, "N", plateau)
        rover.execute_commands("M")
        assert rover.y == 3

    def test_complex_command_sequence(self):
        plateau = Plateau(10, 10)
        rover = Rover(5, 5, "N", plateau)

        # Move in a square pattern
        rover.execute_commands("MMRMMMRMMMRMM")
        # Let's trace: Start(5,5,N) -> MM(5,7,N) -> R(5,7,E) -> MMM(8,7,E) -> R(8,7,S) -> MMM(8,4,S) -> R(8,4,W) -> MM(6,4,W)

        assert rover.x == 6
        assert rover.y == 4
        assert rover.heading == "W"

    def test_boundary_collision_in_sequence(self):
        plateau = Plateau(5, 5)
        rover = Rover(0, 0, "S", plateau)

        # Try to move south and west from corner
        rover.execute_commands("MMLMM")
        # Let's trace: Start(0,0,S) -> M(can't move south, stays 0,0,S) -> M(still can't, 0,0,S) -> L(0,0,E) -> MM(2,0,E)

        # Should stay in bounds
        assert rover.x == 2
        assert rover.y == 0
        assert rover.heading == "E"


class TestRoverEdgeCases:
    """Test edge cases and error conditions"""

    def test_rover_at_corner_movements(self):
        plateau = Plateau(2, 2)

        # Test all corners
        corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
        directions = ["N", "E", "S", "W"]

        for x, y in corners:
            for direction in directions:
                rover = Rover(x, y, direction, plateau)
                rover.move()  # Should not crash
                # Verify rover stays within bounds
                assert plateau.is_within_bounds(rover.x, rover.y)

    def test_position_string_format(self):
        plateau = Plateau(5, 5)
        rover = Rover(1, 2, "N", plateau)
        assert rover.get_position() == "1 2 N"

        rover.move()
        assert rover.get_position() == "1 3 N"

        rover.turn_right()
        assert rover.get_position() == "1 3 E"