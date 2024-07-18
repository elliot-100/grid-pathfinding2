"""Run a demo."""

import logging

from pathfinding.agent import Agent
from pathfinding.grid import Grid
from pathfinding.grid_ref import GridRef
from pathfinding.image_renderer import GridRenderer

AGENT_COUNT = 100


def run() -> None:
    """Create a Grid, bind a Display and run it."""
    logging.basicConfig(level=logging.INFO)

    grid = Grid(64, 64)
    grid.untraversable_locations.extend(
        [
            GridRef(5, 2),
            GridRef(5, 3),
            GridRef(6, 2),
            GridRef(6, 3),
        ]
    )
    agents = [
        Agent(
            grid,
            location=grid.random_location(),
        )
        for _ in range(AGENT_COUNT)
    ]
    for count, agent in enumerate(agents):
        agent.goal = grid.random_location()
        path = agent.uniform_cost_search()
        for location in path:
            grid.traversed.add(location)

        log_msg = f"search {count}/{AGENT_COUNT} complete."
        logging.info(log_msg)

    renderer = GridRenderer(grid, scale=8)
    renderer.show()


if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    run()
