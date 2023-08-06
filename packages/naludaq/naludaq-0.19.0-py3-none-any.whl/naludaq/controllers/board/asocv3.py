"""
"""
from logging import getLogger

from naludaq.helpers import type_name
from naludaq.helpers.semiton import SemitonABC

from .default import BoardController

LOGGER = getLogger("naludaq.board_controller_default")


class BoardControllerAsocv3(SemitonABC, BoardController):
    def toggle_trigger(self, cycles: int = 3):
        """Toggle the trigger signal."""
        if not isinstance(cycles, int):
            raise TypeError(f'"cycles" must be an int, not {type_name(cycles)}')
        if cycles < 1:
            raise ValueError(f'"cycles" must be at least 1, got {cycles}')
        if cycles > 2**16 - 1:
            raise ValueError(
                f'"cycles" must be at most {2**16 - 1} (16-bits), got {cycles}'
            )

        LOGGER.debug("Sending software trigger")
        cmd = f"C000{cycles:04X}"
        self._send_command(cmd)
