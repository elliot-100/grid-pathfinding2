"""Run a demo."""

import logging

from pathfinding.agent import Agent
from pathfinding.grid import Grid
from pathfinding.grid_ref import GridRef

WINDOW_SIZE = 800, 600
WINDOW_CAPTION = "Pathfinding demo"


def run() -> None:
    """Create a Grid, bind a Display and run it."""
    logging.basicConfig(level=logging.INFO)

    grid = Grid(10, 10)
    agent0 = Agent(
        grid,
        location=GridRef(6, 7),
    )
    agent0.goal = GridRef(5, 0)
    search0 = agent0.uniform_cost_search()

    agent1 = Agent(
        grid,
        location=GridRef(8, 2),
    )
    agent1.goal = GridRef(1, 5)
    search1 = agent1.uniform_cost_search()

    log_msg = f"search result: {search0}"
    logger.info(log_msg)
    log_msg = f"search result: {search1}"
    logger.info(log_msg)
    log_msg = grid.text_render()
    logger.info(log_msg)


if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    run()
