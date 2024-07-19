"""Tests for Agent class."""

import pytest

from pathfinding.agent import Agent
from pathfinding.grid import Grid
from pathfinding.grid_ref import GridRef


def test_create_happy_path() -> None:
    """Test that Agent is created as expected."""
    # arrange
    grid0 = Grid(2, 2)

    # act
    agent0 = Agent(
        grid0,
        GridRef(1, 1),
    )
    # assert
    assert agent0.grid == grid0
    assert agent0.location == GridRef(1, 1)
    assert agent0.goal is None
    assert grid0.agents == {agent0}


def test_agent_not_within_grid_bounds_raises_exception() -> None:
    """Test that an exception is raised if agent is created outside grid bounds."""
    # arrange
    grid0 = Grid(2, 2)

    # act, assert
    with pytest.raises(IndexError):
        agent0 = Agent(
            grid0,
            GridRef(1, 2),
        )


def test_uniform_cost_search__happy_path() -> None:
    """Test that a trivial search is calculated correctly."""
    # arrange
    grid0 = Grid(3, 3)
    agent0 = Agent(
        grid0,
        GridRef(0, 0),
    )
    agent0.goal = GridRef(2, 2)

    # act
    search = agent0.uniform_cost_search()

    # assert
    assert search == [
        GridRef(0, 0),
        GridRef(1, 1),
        GridRef(2, 2),
    ]
