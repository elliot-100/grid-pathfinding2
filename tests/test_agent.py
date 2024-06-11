"""Tests for Agent class."""

import pytest

from pathfinding.agent import Agent
from pathfinding.grid import Grid
from pathfinding.grid_ref import GridRef


def test_agent_not_within_grid_bounds_raises_exception() -> None:
    """Test that an exception is raised if agent is created outside grid bounds."""
    # arrange
    grid = Grid(2, 2)

    # act, assert
    with pytest.raises(IndexError):
        agent = Agent(grid, GridRef(1, 2))


def test_uniform_cost_search__happy_path() -> None:
    """Test that a trivial search is calculated correctly."""
    # arrange
    grid = Grid(3, 3)
    agent = Agent(
        grid,
        GridRef(0, 0),
    )
    # act
    search = agent.uniform_cost_search(GridRef(2, 2))

    # assert
    assert search == [
        GridRef(1, 1),
        GridRef(0, 0),
    ]
