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
        self.cost_so_far = {self.location: 0}

        came_from: dict[GridRef, GridRef | None] = {self.location: None}
        frontier: _PriorityQueue = _PriorityQueue()
        frontier.put(0, self.location)

        while not frontier.is_empty:
            current_location = frontier.get()

            if current_location == self.goal:  # early exit
                break

            for new_location in self.grid.neighbours(current_location):
                new_cost = self._cost(current_location, new_location)
                if (
                    new_location not in came_from
                    or new_cost < self.cost_so_far[new_location]
                    # add new_location to frontier if cheaper
                ):
                    self.cost_so_far[new_location] = new_cost
                    frontier.put(priority=new_cost, location=new_location)
                    came_from[new_location] = current_location

        # Construct path starting at goal and retracing to agent location...
        self.path_to_goal = {self.goal}
        current_location = self.goal

        while current_location is not self.location:
            came_from_location = came_from.get(current_location)
            if came_from_location is None:
                err_msg = "`came_from_location` unexpectedly `None`."
                raise TypeError(err_msg)
            current_location = came_from_location
            self.path_to_goal.add(current_location)

        return self.path_to_goal

    def _cost(
        self,
        from_location: GridRef,
        to_location: GridRef,
    ) -> float:
        """Currently just wraps Grid.cost(), but to be expanded."""
        return self.cost_so_far[from_location] + self.grid.cost(  # type: ignore[index]
            from_location, to_location,
        )
