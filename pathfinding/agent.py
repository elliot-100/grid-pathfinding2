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
        """Reference to a `.grid.Grid` instance."""
        self.location = location

        if not self.grid.in_bounds(self.location):
            err_msg = f"Location {self.location} not on grid."
            raise IndexError(err_msg)

        self.goal: GridRef | None = None
        """Needs to be set directly, at present."""
        self.path_to_goal: set[GridRef] = set()
        """Locations on the path to goal.
        Set indirectly by `Agent.uniform_cost_search()` at present."""

        self.grid.agents.add(self)

    def uniform_cost_search(
        self,
    ) -> set[GridRef]:
        """Perform uniform cost search for`self.goal`.

        Variation of Dijkstra's algorithm.

        Returns
        -------
        set[GridRef]
            Locations on the path to `self.goal`.
            Empty if no path found.
        """
        if self.goal is None:
            raise ValueError
        if self.goal == self.location:
            return {self.location}
        if (
            self.location in self.grid.untraversable_locations
            or self.goal in self.grid.untraversable_locations
        ):
            return set()

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
        self.path_to_goal = {self.goal}
        current_location = self.goal

        while current_location is not self.location:
            came_from_location = came_from.get(current_location)
            if came_from_location is None:
                return set()
            current_location = came_from_location
            self.path_to_goal.add(current_location)

        return self.path_to_goal
