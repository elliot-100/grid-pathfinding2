"""Agent class."""

from dataclasses import dataclass, field

from .grid import Grid
from .grid_ref import GridRef
from .priority_queue import _PriorityQueue


@dataclass
class Agent:
    """Agent class.

    Public attributes
    -----------------
    grid: Grid
    location: GridRef
    """

    grid: Grid
    location: GridRef

    _came_from: dict[GridRef, GridRef | None] = field(default_factory=dict, init=False)
    _cost_so_far: dict[GridRef, float] = field(default_factory=dict, init=False)

    def __post_init__(self) -> None:
        if not self.grid.in_bounds(self.location):
            err_msg = f"Location {self.location} not on grid."
            raise IndexError(err_msg)

    def uniform_cost_search(
        self,
        goal_location: GridRef,
    ) -> list[GridRef]:
        """Perform uniform cost search (variation of Dijkstra's algorithm).

        Parameters
        ----------
        goal_location: GridRef

        Returns
        -------
        list[GridRef]
            Path to `goal_location` as a list of locations.
            Empty list if no path found.
        """
        self._came_from[self.location] = None
        self._cost_so_far[self.location] = 0

        frontier: _PriorityQueue = _PriorityQueue()
        frontier.put(0, self.location)

        while not frontier.is_empty:
            current_location = frontier.get()

            if current_location == goal_location:  # early exit
                break

            for new_location in self.grid.neighbours(current_location):
                new_cost = self._cost_so_far[current_location] + self.grid.cost(
                    current_location, new_location
                )
                if (
                    new_location not in self._came_from
                    or new_cost < self._cost_so_far[new_location]
                    # add new_location to frontier if cheaper
                ):
                    self._cost_so_far[new_location] = new_cost
                    frontier.put(priority=new_cost, location=new_location)
                    self._came_from[new_location] = current_location

        # Construct path starting at goal and retracing to agent location...
        path_to_goal: list[GridRef] = [goal_location]
        location = goal_location
        while location is not self.location:
            # TO DO:  Incompatible types in assignment (expression has type "GridRef |
            # None", variable has type "GridRef")
            location = self._came_from.get(location)  # type: ignore[assignment]
            path_to_goal.append(location)
        return list(reversed(path_to_goal))
