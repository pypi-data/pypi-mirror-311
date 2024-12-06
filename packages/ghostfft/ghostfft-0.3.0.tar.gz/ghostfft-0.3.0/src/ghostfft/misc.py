import numpy as np

from .component import Component
from .fp import rightshift


class ShiftRight(Component):
    """
    Shift data to the right. Does not change the bitwidth.

    :bwin: The bit width of the input data array.
    :shift: The number of positions to shift the data.
    """
    def __init__(self, bwin: int, shift: int):
        super().__init__(bwin, bwin)
        self.shift = shift

    def _impl(self, bdatain: np.ndarray = None, **kwargs):
        self.bdataout = rightshift(bdatain, self.shift)


class ShiftLeft(Component):
    """
    Shift data to the left. Does not change the bitwidth.

    :bwin: The bit width of the input data array.
    :shift: The number of positions to shift the data.
    """
    def __init__(self, bwin: int, shift: int):
        super().__init__(bwin, bwin)
        self.shift = shift

    def _impl(self, bdatain: np.ndarray = None, **kwargs):
        self.bdataout = bdatain << self.shift
