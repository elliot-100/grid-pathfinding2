"""Grid class."""

from __future__ import annotations

import math
import random
from typing import TYPE_CHECKING

from .grid_ref import GridRef

if TYPE_CHECKING:
    from .agent import Agent

CARDINAL_DIRECTIONS = {(1, 0), (0, 1), (-1, 0), (0, -1)}
DIAGONAL_DIRECTIONS = {(1, 1), (-1, 1), (-1, -1), (1, -1)}


class Grid:
    """Rectangular Grid class.

    Public attributes
    -----------------
    size_x: int
    size_y: int
    allow_diagonal_moves: bool, default True
    untraversable_locations: list[GridRef]
        List of locations which cannot be traversed.
    traversed: list[GridRef]
        List of locations which have been traversed.
        Currently populated externally.

    Non-public/internal attributes
    ------------------------------
    _directions: set[GridRef]
        Allowed directional moves.
    """

    def __init__(
        self,
        size_x: int,
        size_y: int,
        *,
        allow_diagonal_moves: bool = True,
    ) -> None:
        self.size_x = size_x
        self.size_y = size_y
        self.allow_diagonal_moves = allow_diagonal_moves

        self.untraversable_locations: list[GridRef] = []
        self.traversed: set[GridRef] = set()

        self._directions = CARDINAL_DIRECTIONS
        if self.allow_diagonal_moves:
            self._directions.update(DIAGONAL_DIRECTIONS)
        self.agents: list[Agent] = []

    def in_bounds(self, location: GridRef) -> bool:
        """Determine whether `location` is within the Grid."""
        return 0 <= location.x < self.size_x and 0 <= location.y < self.size_y

    def random_location(self, *, allow_untraversable: bool = False) -> GridRef:
        """Return a random location on the Grid.

        By default, don't allow untraversable locations.

        """
        location = GridRef(
            random.randint(0, self.size_x - 1), random.randint(0, self.size_y - 1)
        )
        if not allow_untraversable and not self.is_traversable(location):
            return self.random_location()
        return location

    def is_traversable(self, location: GridRef) -> bool:
        """Determine whether `location` is traversable."""
        return location not in self.untraversable_locations

    def neighbours(self, location: GridRef) -> set[GridRef]:
        """Return reachable neighbours of `location`."""
        reachable_neighbours: set[GridRef] = set()

        if location in self.untraversable_locations:
            return reachable_neighbours

        for dir_ in self._directions:
            neighbour = GridRef(location.x + dir_[0], location.y + dir_[1])
            if self.in_bounds(neighbour) and self.is_traversable(neighbour):
                reachable_neighbours.add(neighbour)
        return reachable_neighbours

    def untraversable_from_map(self, grid_map: list[str]) -> list[GridRef]:
        """Set `Grid.untraversable_locations` from 'X's in text representation.

        Does not set grid dimensions. Out of bounds locations are ignored.

        Returns
        -------
        List of locations.

        Example `grid_map` = [
            "X..X",
            ".X",
            "..X",
            ]
        """
        self.untraversable_locations = []
        for y, row in enumerate(grid_map):
            self.untraversable_locations.extend(
                GridRef(x, y)
                for x, cell in enumerate(row)
                if cell == "X" and self.in_bounds(GridRef(x, y))
            )
        return self.untraversable_locations

    def cost(self, from_location: GridRef, to_location: GridRef) -> float:
        """Calculate the cost as Euclidean distance from one location to another.

        NB: when calculating next step in a search, locations will be adjacent, so a
        cardinal move has basic cost = 1, and diagonal basic cost =~ 1.4.
        This function is generalised for wider use.

        """
        x_dist = abs(from_location.x - to_location.x)
        y_dist = abs(from_location.y - to_location.y)
        cost = math.sqrt(x_dist**2 + y_dist**2)

        if to_location in self.traversed:
            cost = cost * 0.5

        return max(cost, 0)

    def text_render(self) -> str:
        """Output a text-based visual representation."""
        output = "\n"
        for y in range(self.size_y):
            for x in range(self.size_x):
                location = GridRef(x, y)
                char = "· "
                if location in self.untraversable_locations:
                    char = "█ "
                for agent in self.agents:
                    if location in agent.path_to_goal:
                        char = "+ "
                    if location == agent.location:
                        char = "A "
                    if location == agent.goal:
                        char = "G "
                output += char
            output += "\n"
        return output
