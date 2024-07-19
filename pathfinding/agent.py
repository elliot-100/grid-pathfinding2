"""Module containing `Agent` class."""

from __future__ import annotations

from typing import TYPE_CHECKING

from ._priority_queue import _PriorityQueue

if TYPE_CHECKING:
    from .grid import Grid
    from .grid_ref import GridRef


class Agent:
    """Agent class."""

    def __init__(self, grid: Grid, location: GridRef) -> None:
        self.grid = grid
        self.location = location

        if not self.grid.in_bounds(self.location):
            err_msg = f"Location {self.location} not on grid."
            raise IndexError(err_msg)

        self.goal: GridRef | None = None
        self.path_to_goal: list[GridRef] = []
        self.grid.agents.add(self)

    def uniform_cost_search(
        self,
    ) -> list[GridRef]:
        """Perform uniform cost search for`self.goal`.

        Variation of Dijkstra's algorithm.

        Returns
        -------
        list[GridRef] :
            Path to `self.goal` as a list of locations.
            Empty list if no path found.
        """
        if self.goal is None:
            raise ValueError
        came_from: dict[GridRef, GridRef | None] = {self.location: None}
        cost_so_far: dict[GridRef, float] = {self.location: 0}
        frontier: _PriorityQueue = _PriorityQueue()
        frontier.put(0, self.location)

        while not frontier.is_empty:
            current_location = frontier.get()

            if current_location == self.goal:  # early exit
                break

            for new_location in self.grid.neighbours(current_location):
                new_cost = cost_so_far[current_location] + self.grid.cost(
                    current_location, new_location
                )
                if (
                    new_location not in came_from
                    or new_cost < cost_so_far[new_location]
                    # add new_location to frontier if cheaper
                ):
                    cost_so_far[new_location] = new_cost
                    frontier.put(priority=new_cost, location=new_location)
                    came_from[new_location] = current_location

        # Construct path starting at goal and retracing to agent location...
        path_from_goal: list[GridRef] = [self.goal]
        location = self.goal
        while location is not self.location:
            if location is None:
                err_msg = "Unexpected error."
                raise ValueError(err_msg)
            # TO DO:  Incompatible types in assignment (expression has type "GridRef |
            # None", variable has type "GridRef")
            location = came_from.get(location)  # type: ignore[assignment]
            path_from_goal.append(location)

        self.path_to_goal = list(reversed(path_from_goal))
        return self.path_to_goal
