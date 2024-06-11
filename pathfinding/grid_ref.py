"""GridRef class."""

from dataclasses import dataclass


@dataclass(frozen=True)  # therefore hashable
class GridRef:
    """Grid Reference class."""

    x: int
    y: int

    @property
    def as_tuple(self) -> tuple[int, int]:
        """Get simple tuple representation for output."""
        return self.x, self.y
