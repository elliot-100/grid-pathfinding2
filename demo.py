"""Run a demo."""

import logging

from pathfinding import log_info
from pathfinding.agent import Agent
from pathfinding.grid import Grid
from pathfinding.grid_ref import GridRef


def run() -> None:
    """Create a Grid, bind a Display and run it."""
    log = logging.getLogger(__name__)
    grid = Grid(10, 10)
    grid.untraversable_locations = {
        GridRef(5, 2),
        GridRef(5, 3),
        GridRef(6, 2),
        GridRef(6, 3),
    }
    agent0 = Agent(
        grid,
        location=GridRef(6, 7),
    )
    agent0.goal = GridRef(5, 0)
    agent0.uniform_cost_search()

    agent1 = Agent(
        grid,
        location=GridRef(8, 2),
    )
    agent1.goal = GridRef(1, 5)
    agent1.uniform_cost_search()

    log_info(log, grid.text_render())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    run()
