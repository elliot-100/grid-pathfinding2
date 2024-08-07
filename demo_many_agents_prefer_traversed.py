"""Run a demo."""

import logging
import time

from pathfinding import log_info
from pathfinding.agent import Agent
from pathfinding.grid import Grid
from pathfinding.grid_ref import GridRef
from pathfinding.image_renderer import GridRenderer

AGENT_COUNT = 100
REPORT_PROGRESS_FACTOR = 0.1


def run() -> None:
    """Create a Grid, bind a Display and run it."""
    log = logging.getLogger(__name__)
    start_time = time.time()

    grid = Grid(64, 64, prefer_traversed_factor=0.5)
    grid.set_untraversable_area(
        GridRef(20, 0),
        GridRef(40, 70),
    )

    agents = [
        Agent(
            grid,
            location=grid.random_location(allow_untraversable=True),
        )
        for _ in range(AGENT_COUNT)
    ]
    log_info(log, "Grid and agents initialised.", start_time)

    progress_reported = 0.0
    for i, agent in enumerate(agents):
        agent.goal = grid.random_location(allow_untraversable=True)
        path = agent.uniform_cost_search()
        grid.shared_path_locations.update(path)

        progress = i / AGENT_COUNT
        if progress >= progress_reported + REPORT_PROGRESS_FACTOR:
            log_info(
                log, f"{i} iterations done; {progress*100:.0f}% complete", start_time
            )
            progress_reported = progress

    log_info(log, f"{AGENT_COUNT} iterations complete.", start_time)
    renderer = GridRenderer(grid, scale=8)
    log_info(log, "Image rendered.", start_time)
    renderer.show()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    run()
