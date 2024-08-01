"""Module containing `GridRenderer` class."""

import logging
import time
from typing import ClassVar

from PIL import Image

from . import log_info
from .grid import Grid
from .grid_ref import GridRef


class GridRenderer:
    """Renders a `.grid.Grid` as a static image."""

    COLOR_MAPPING: ClassVar = {
        "EMPTY": (128, 128, 128),  # pygame 'grey50'
        "BLOCK": (104, 104, 104),  # pygame 'grey50'
        "START": (0, 139, 0),  # pygame 'green4'
        "GOAL": (238, 0, 0),  # pygame 'red2'
        "ON_PATH": (255, 193, 37),  # pygame 'goldenrod1'
    }

    def __init__(
        self,
        grid: Grid,
        scale: int = 32,
    ) -> None:
        """Create a new GridRenderer instance."""
        log = logging.getLogger(__name__)
        start_time = time.time()
        self.grid = grid
        self._image = Image.new(
            mode="RGB",  # 3x8-bit pixels, true color
            size=(self.grid.size_x, self.grid.size_y),
        )
        # populate pixels
        log_info(log, "Calculating pixels...", start_time)
        pixels = [
            self._pixel_color(x, y)
            for x in range(self.grid.size_x)
            for y in range(self.grid.size_y)
        ]
        log_info(log, "Done.", start_time)
        self._image.putdata(pixels)
        # resize for output
        self._image = self._image.resize(
            size=(scale * grid.size_x, scale * self.grid.size_y),
            resample=Image.Resampling.NEAREST,
        )

    def _pixel_color(self, x: int, y: int) -> tuple[int, int, int]:
        """Determine the pixel colour."""
        location = GridRef(x, y)
        for agent in self.grid.agents:
            if location == agent.goal:
                return self.COLOR_MAPPING["GOAL"]  # type: ignore[no-any-return]
            if location == agent.location:
                return self.COLOR_MAPPING["START"]  # type: ignore[no-any-return]
            if location in agent.path_to_goal:
                return self.COLOR_MAPPING["ON_PATH"]  # type: ignore[no-any-return]
        if location in self.grid.untraversable_locations:
            return self.COLOR_MAPPING["BLOCK"]  # type: ignore[no-any-return]
        return self.COLOR_MAPPING["EMPTY"]  # type: ignore[no-any-return]

    def show(
        self,
    ) -> None:
        """Show the image."""
        self._image.show()
