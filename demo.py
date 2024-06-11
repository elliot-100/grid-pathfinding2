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
    agent = Agent(
        grid,
        GridRef(3, 7),
    )
    search = agent.uniform_cost_search(GridRef(9, 9))
    log_msg = f"search result: {search}"
    logger.info(log_msg)


if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    run()
