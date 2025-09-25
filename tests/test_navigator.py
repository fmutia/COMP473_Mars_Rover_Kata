import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from hexrover.adapters.grid_nav import Plateau, GridNavigator
from hexrover.adapters.collision_nav import CollisionNavigator, Occupancy
from hexrover.ports import Position, Heading


def test_grid_navigator_forward_and_turns():
    plateau = Plateau(5, 5)
    nav = GridNavigator(plateau)

    # move from origin east -> (1,0)
    p0 = Position(0, 0)
    assert nav.forward(p0, Heading.E) == Position(1, 0)

    # safe stop at north-east corner when moving north
    corner = Position(5, 5)
    assert nav.forward(corner, Heading.N) == corner

    # turning behavior
    assert nav.turn_left(Heading.N) == Heading.W
    assert nav.turn_right(Heading.N) == Heading.E


def test_collision_navigator_blocks_and_allows_moves_and_delegates_turns():
    plat = Plateau(5, 5)
    inner = GridNavigator(plat)

    # occupied target by another actor -> move blocked
    occ_blocking = Occupancy(positions={
        "self": Position(0, 0),
        "other": Position(1, 0),
    })
    col_nav = CollisionNavigator(inner=inner, occ=occ_blocking, self_id="self")
    assert col_nav.forward(Position(0, 0), Heading.E) == Position(0, 0)

    # unoccupied target -> move allowed
    occ_free = Occupancy(positions={
        "self": Position(0, 0),
        "other": Position(5, 5),
    })
    col_nav2 = CollisionNavigator(inner=inner, occ=occ_free, self_id="self")
    assert col_nav2.forward(Position(0, 0), Heading.E) == Position(1, 0)

    # turns delegated to inner navigator
    assert col_nav2.turn_left(Heading.N) == inner.turn_left(Heading.N)
    assert col_nav2.turn_right(Heading.N) == inner.turn_right(Heading.N)