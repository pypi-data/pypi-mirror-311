import numpy as np

from .fp import FixedPoint


class UFixedPoint(FixedPoint):
    """
    Modifies behaviour of FixedPoint to represent an unsigned fixed point.
    """

    def __neg__(self):
        raise RuntimeError("The UFixedPoint cannot be negated.")

    def __sub__(self, other):
        raise RuntimeError("The UFixedPoint cannot be subtracted.")

    def mask_bitwidth(self, bdata: np.ndarray = None) -> np.ndarray:
        """
        Applies mask keeping all the extra left bits zero. This allows to keep interpreting
        the MSB as positive part.

        :param bdata: Array to be masked. If None, self.bdata will be masked.
        :return: Array masked.
        """
        if bdata is None:
            bdata = self.bdata

        mask = (1 << self.bw) - 1
        return bdata & mask

    def _handle_overflow(self, bdata: np.ndarray):
        if self.ofmode == "saturate":
            min_value = 0
            max_value = (1 << self.bw) - 1
            return np.clip(bdata, min_value, max_value)
        return bdata

    def from_float(self, data: np.ndarray):
        """
        Convert the provided floating point number or numpy array into
        its fixed-point representation according to the bit width and
        binary point of this data type.

        :param data: Array to be converted.
        :return: Data array in binary format.
        """
        if np.any(data < 0):
            self.logger.warning("Negative values in UFixedPoint.from_float(). Possible data loss.")

        return super().from_float(data)
