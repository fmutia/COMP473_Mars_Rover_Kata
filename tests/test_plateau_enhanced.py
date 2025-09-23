import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from hexrover.compat.plateau_compat import Plateau


def test_plateau_creation():
    """Test plateau creation with various sizes"""
    plateau = Plateau(5, 5)
    assert plateau.max_x == 5
    assert plateau.max_y == 5

    plateau_large = Plateau(100, 200)
    assert plateau_large.max_x == 100
    assert plateau_large.max_y == 200


def test_plateau_bounds_corners():
    """Test all corner cases of plateau boundaries"""
    plateau = Plateau(5, 5)

    # Test corners
    assert plateau.is_within_bounds(0, 0)  # Bottom-left
    assert plateau.is_within_bounds(5, 0)  # Bottom-right
    assert plateau.is_within_bounds(0, 5)  # Top-left
    assert plateau.is_within_bounds(5, 5)  # Top-right


def test_plateau_bounds_edges():
    """Test boundary edge cases"""
    plateau = Plateau(5, 5)

    # Test edges
    assert plateau.is_within_bounds(2, 0)  # Bottom edge
    assert plateau.is_within_bounds(2, 5)  # Top edge
    assert plateau.is_within_bounds(0, 2)  # Left edge
    assert plateau.is_within_bounds(5, 2)  # Right edge


def test_plateau_bounds_outside():
    """Test positions outside plateau bounds"""
    plateau = Plateau(5, 5)

    # Test outside bounds
    assert not plateau.is_within_bounds(-1, 0)  # Left of plateau
    assert not plateau.is_within_bounds(6, 0)  # Right of plateau
    assert not plateau.is_within_bounds(0, -1)  # Below plateau
    assert not plateau.is_within_bounds(0, 6)  # Above plateau

    # Test far outside bounds
    assert not plateau.is_within_bounds(-10, -10)
    assert not plateau.is_within_bounds(100, 100)


def test_single_cell_plateau():
    """Test edge case of 1x1 plateau"""
    plateau = Plateau(0, 0)
    assert plateau.is_within_bounds(0, 0)
    assert not plateau.is_within_bounds(1, 0)
    assert not plateau.is_within_bounds(0, 1)
