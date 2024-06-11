"""Grid class."""

import math
from dataclasses import dataclass, field

from .grid_ref import GridRef

CARDINAL_DIRECTIONS = {(1, 0), (0, 1), (-1, 0), (0, -1)}
DIAGONAL_DIRECTIONS = {(1, 1), (-1, 1), (-1, -1), (1, -1)}


@dataclass
class Grid:
    """Rectangular Grid class.

    Public attributes
    -----------------
    size_x: int
    size_y: int
    allow_diagonal_moves: bool, default True
    untraversable_locations: list[GridRef]
        List of locations which cannot be traversed.

    Non-public/internal attributes
    ------------------------------
    _directions: set[GridRef]
        Allowed directional moves.
    """

    # Set by init:
    size_x: int
    size_y: int
    allow_diagonal_moves: bool = True
    untraversable_locations: list[GridRef] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Set allowable directions."""
        self._directions = CARDINAL_DIRECTIONS
        if self.allow_diagonal_moves:
            self._directions.update(DIAGONAL_DIRECTIONS)

    def in_bounds(self, location: GridRef) -> bool:
        """Determine whether `location` is within the Grid."""
        return 0 <= location.x < self.size_x and 0 <= location.y < self.size_y

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

    @staticmethod
    def cost(location1: GridRef, location2: GridRef) -> float:
        """Calculate the cost as Euclidean distance between two locations."""
        x_dist = abs(location1.x - location2.x)
        y_dist = abs(location1.y - location2.y)
        return math.sqrt(x_dist**2 + y_dist**2)
