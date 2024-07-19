"""Tests for Grid class."""

from pathfinding.grid import Grid
from pathfinding.grid_ref import GridRef


def test_create_happy_path() -> None:
    """Test that Grid is created as expected."""
    # arrange
    # act
    grid0 = Grid(8, 7)

    # assert
    assert grid0.size_x == 8
    assert grid0.size_y == 7
    assert grid0.allow_diagonal_moves is True
    assert grid0.untraversable_locations == set()
    assert grid0._directions == {
        (-1, -1),
        (-1, 0),
        (-1, 1),
        (0, -1),
        (0, 1),
        (1, -1),
        (1, 0),
        (1, 1),
    }
    assert grid0.agents == set()


def test_neighbours_not_at_edge() -> None:
    """Test that all neighbours are returned for a mid-grid location."""
    # arrange
    grid0 = Grid(10, 10)
    loc0 = GridRef(4, 5)

    # act
    n = grid0.neighbours(loc0)

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
    grid0 = Grid(10, 10)
    loc0 = GridRef(0, 0)
    loc1 = GridRef(9, 9)

    # act
    n0 = grid0.neighbours(loc0)
    n1 = grid0.neighbours(loc1)

    # assert
    assert n0 == {GridRef(1, 0), GridRef(1, 1), GridRef(0, 1)}
    assert n1 == {GridRef(8, 9), GridRef(8, 8), GridRef(9, 8)}


def test_untraversable_from_map() -> None:
    """TO DO."""
    # arrange
    grid0 = Grid(10, 10)
    block_map = [
        "X..X",
        ".X..",
        "..X.",
    ]

    # act
    grid0.set_untraversable_from_map(block_map)

    # assert
    assert grid0.untraversable_locations == {
        GridRef(0, 0),
        GridRef(3, 0),
        GridRef(1, 1),
        GridRef(2, 2),
    }
