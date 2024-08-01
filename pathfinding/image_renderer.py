"""Module containing `GridRenderer` class."""

import logging
import time
from typing import ClassVar

from PIL import Image

from . import log_info
from ._pygame_colordict import THECOLORS
from .grid import Grid
from .grid_ref import GridRef


class GridRenderer:
    """Renders a `.grid.Grid` as a static image."""

    _COLOR_MAPPING: ClassVar = {
        "EMPTY": THECOLORS["grey50"],
        "BLOCK": THECOLORS["grey40"],
        "AGENT_START": THECOLORS["green4"],
        "AGENT_GOAL": THECOLORS["red2"],
        "ON_AGENT_PATH": THECOLORS["goldenrod1"],
    }

    def __init__(
        self,
        grid: Grid,
        scale: int = 32,
    ) -> None:
        """Create a new `GridRenderer` instance bound to `grid`."""
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
        color = self._COLOR_MAPPING["EMPTY"]

        for agent in self.grid.agents:
            if location in agent.path_to_goal:
                color = self._COLOR_MAPPING["ON_AGENT_PATH"]
            if location == agent.location:
                color = self._COLOR_MAPPING["AGENT_START"]
            if location == agent.goal:
                color = self._COLOR_MAPPING["AGENT_GOAL"]

        if location in self.grid.untraversable_locations:
            color = self._COLOR_MAPPING["BLOCK"]
        return color  # type: ignore[no-any-return]

    def show(
        self,
    ) -> None:
        """Show the image."""
        self._image.show()

    def save(
        self,
        filename: str,
    ) -> None:
        """Save the image."""
        self._image.save(filename)
