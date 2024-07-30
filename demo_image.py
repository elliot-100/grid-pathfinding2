"""Run a demo."""

from pathfinding.agent import Agent
from pathfinding.grid import Grid
from pathfinding.grid_ref import GridRef
from pathfinding.image_renderer import GridRenderer


def run() -> None:
    """Create a Grid, bind a Display and run it."""
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

    renderer = GridRenderer(grid)
    renderer.show()


if __name__ == "__main__":
    run()
