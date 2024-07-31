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
        self.cost_so_far: dict[GridRef, float] = {self.location: 0}
        self.grid.agents.add(self)

    def uniform_cost_search(
        self,
        prefer_existing_paths_factor: float = 0,
    ) -> set[GridRef]:
        """Perform uniform cost search for`self.goal`.

        Variation of Dijkstra's algorithm.

        Parameters
        ----------
        prefer_existing_paths_factor :
              A 'discount factor' for using a location on previous paths.

        Returns
        -------
        set[GridRef]
            Locations on the path to `self.goal`.
            Empty if no path found.
        """
        if self.goal is None:
            raise ValueError
        came_from: dict[GridRef, GridRef | None] = {self.location: None}

        frontier: _PriorityQueue = _PriorityQueue()
        frontier.put(0, self.location)

        while not frontier.is_empty:
            current_location = frontier.get()

            if current_location == self.goal:  # early exit
                break

            for new_location in self.grid.neighbours(current_location):
                new_cost = self.cost_so_far[current_location] + self.grid.cost(
                    current_location, new_location
                )
                if new_location in self.grid.traversed:
                    new_cost = new_cost * (1 - prefer_existing_paths_factor)
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
        prefer_existing_paths_factor: float,
    ) -> float:
        if from_location == to_location:
            raise ValueError
        cost = self.cost_so_far[from_location] + self.grid.cost(
            from_location, to_location
        )
        # apply discount for using existing paths
        if to_location in self.grid.traversed:
            cost = cost * (1 - prefer_existing_paths_factor)
        print(cost)
        return cost
