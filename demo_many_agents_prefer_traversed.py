"""Run a demo."""

import logging
import time

from pathfinding import log_info
from pathfinding.agent import Agent
from pathfinding.grid import Grid
from pathfinding.grid_ref import GridRef
from pathfinding.image_renderer import GridRenderer

AGENT_COUNT = 100


def run() -> None:
    """Create a Grid, bind a Display and run it."""
    log = logging.getLogger(__name__)
    start_time = time.time()

    grid = Grid(64, 64, prefer_traversed_factor=0.5)
    grid.untraversable_locations = {
        GridRef(5, 2),
        GridRef(5, 3),
        GridRef(6, 2),
        GridRef(6, 3),
    }

    agents = [
        Agent(
            grid,
            location=grid.random_location(),
        )
        for _ in range(AGENT_COUNT)
    ]
    log_info(log, "Grid and agents initialised.", start_time)

    for agent in agents:
        agent.goal = grid.random_location()
        path = agent.uniform_cost_search()
        for location in path:
            grid.traversed.add(location)

    log_info(log, f"{AGENT_COUNT} iterations complete.", start_time)
    renderer = GridRenderer(grid, scale=8)
    renderer.show()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    run()
