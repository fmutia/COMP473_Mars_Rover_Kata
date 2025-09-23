import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from hexrover.compat.plateau_compat import Plateau

def test_plateau_bounds():
    plateau = Plateau(5, 5)
    assert plateau.is_within_bounds(0, 0)
    assert plateau.is_within_bounds(5, 5)
    assert not plateau.is_within_bounds(6, 5)
    assert not plateau.is_within_bounds(5, 6)
