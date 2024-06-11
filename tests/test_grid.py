"""Tests for Grid class."""

from pathfinding.grid import Grid
from pathfinding.grid_ref import GridRef


def test_neighbours_not_at_edge() -> None:
    """Test that all neighbours are returned for a mid-grid location."""
    # arrange
    grid = Grid(10, 10)
    loc = GridRef(4, 5)

    # act
    n = grid.neighbours(loc)

    # assert
    assert n == {
        GridRef(3, 4),
        GridRef(3, 5),
        GridRef(3, 6),
        GridRef(4, 4),
        GridRef(4, 6),
        GridRef(5, 4),
        GridRef(5, 5),
        GridRef(5, 6),
    }


def test_neighbours_at_edges() -> None:
    """TO DO."""
    # arrange
    grid = Grid(10, 10)
    loc0 = GridRef(0, 0)
    loc1 = GridRef(9, 9)

    # act
    n0 = grid.neighbours(loc0)
    n1 = grid.neighbours(loc1)

    # assert
    assert n0 == {GridRef(1, 0), GridRef(1, 1), GridRef(0, 1)}
    assert n1 == {GridRef(8, 9), GridRef(8, 8), GridRef(9, 8)}


def test_untraversable_from_map() -> None:
    """TO DO."""
    # arrange
    grid = Grid(10, 10)
    grid_map = [
        "X..X",
        ".X..",
        "..X.",
    ]

    # act
    coordinates = grid.untraversable_from_map(grid_map)

    # assert
    assert coordinates == [
        GridRef(0, 0),
        GridRef(3, 0),
        GridRef(1, 1),
        GridRef(2, 2),
    ]
