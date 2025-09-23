import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from main import run_simulation


class TestIntegration:
    """Integration tests for the complete system"""

    def test_original_example(self):
        """Test the original kata example"""
        input_str = """5 5
1 2 N
LMLMLMLMM
3 3 E
MMRMMRMRRM"""

        expected = """1 3 N
5 1 E"""

        result = run_simulation(input_str)
        assert result == expected

    def test_single_rover(self):
        """Test with only one rover"""
        input_str = """3 3
1 1 E
MMM"""

        expected = "3 1 E"

        result = run_simulation(input_str)
        assert result == expected

    def test_rover_stays_in_place(self):
        """Test rover that only rotates"""
        input_str = """5 5
2 2 N
LLLL"""

        expected = "2 2 N"  # Full rotation, back to North

        result = run_simulation(input_str)
        assert result == expected

    def test_boundary_collision_scenario(self):
        """Test rovers trying to move out of bounds"""
        input_str = """2 2
0 0 S
MMMMM
2 2 N
MMMMM"""

        expected = """0 0 S
2 2 N"""  # Both should stay at boundaries

        result = run_simulation(input_str)
        assert result == expected

    def test_large_plateau(self):
        """Test with a larger plateau"""
        input_str = """10 10
0 0 N
MMMMMMMMMM
10 0 W
MMMMMMMMMM"""

        expected = """0 10 N
0 0 W"""

        result = run_simulation(input_str)
        assert result == expected

    def test_complex_path(self):
        """Test a complex rover path"""
        input_str = """5 5
2 2 N
MRMLMRMLMRM"""

        result = run_simulation(input_str)
        # Verify result is in correct format
        assert len(result.split()) == 3
        x, y, heading = result.split()
        assert x.isdigit() and y.isdigit()
        assert heading in ["N", "E", "S", "W"]
