from typing import Callable, Literal

import numpy as np

from .component import Component
from .fp import FixedPoint


class PFB(Component):
    """
    A model of CASPER PFB.

    :bwin: The bit width of the input data array.
    :bwout: The bit width of the output data array.
    :param logsize: Size of the FFT (2**fft_size points)
    :param ntaps: Total number of taps in the PFB
    :param logninputs: Number of parallel input streams
    :param window: The window function to use. Must have signature: window(n_points).
    :param quantization: Mode of quantization when casting result of PFB multiplication and sum to the
                         selected output configuration. "inf" mode resolves ties away from zero to
                         +/- infinity. "even" resolves ties to nearest even number. "truncate" disables
                         rounding.
    :datalog: If True, the component data output is logged.
    """

    def __init__(self, logsize: int, ntaps: int, logninputs: int, window: Callable = np.hamming,
                 bwin: int = 8, bwout: int = 18, bwcoef: int = 18,
                 quantization: Literal["inf", "even", "truncate"] = "inf",
                 debug_flag: int = None, **kwargs):
        super().__init__(bwin, bwout, **kwargs)
        self.logger.info(
            f"Initializing {self.__class__.__name__} core with logsize={logsize}, ntaps={ntaps}, "
            f"logninputs={logninputs}, window={getattr(window, '__name__', repr(window))}")
        self.logsize = logsize
        self.ntaps = ntaps
        self.logninputs = logninputs
        self.tapsize = 2 ** (logsize - logninputs)
        self.window = window
        self.quantization = quantization

        self.taps = FixedPoint(bwin, bwin - 1, np.zeros((2 ** logninputs, ntaps * self.tapsize)))
        self.tc_count = -1
        self.bdataout = None

        self.debug_flag = debug_flag

        tapscoef = np.empty((2 ** logninputs, ntaps, self.tapsize))

        for i in range(2 ** logninputs):
            for j in range(ntaps):
                # Taps use inverse order of coefficients sets (the last part of the window
                # is used in a first tap and so on)
                tapscoef[i, j] = self.coef_gen_calc(i, ntaps - j - 1)

        self.tapscoef = FixedPoint(bwcoef, bwcoef - 1, tapscoef)

    def _impl(self, bdatain: np.ndarray = None, **kwargs):
        if bdatain.size != 2 ** self.logninputs:
            raise ValueError(
                f'Invalid input data_ shape. Input array must be 1D and have {2 ** self.logninputs} elements')
        # Shifting data_ in taps and adding new data
        self.taps = self.taps.shift_insert(bdatain)

        # Windowing and summing taps
        tapout = self.taps[:, ::self.tapsize]
        coefout = self.tapscoef[:, :, self.tc_count]
        if tapout.shape != coefout.shape:
            raise RuntimeError(f"Shapes of taps {tapout.shape} and coefficients {coefout.shape} "
                               f"slices shapes do not match. Check the inner algorithm")

        tapxcoef = tapout * coefout

        if self.debug_flag == 1:
            self.debug_data = tapout, coefout, tapxcoef

        # After each addition the sum gets shifted right by 1 position
        # so the fpt_dataout type remains he same. The number of additions
        # (and shifts) is ceil(log2(ntaps))
        tapxcoefsum = tapxcoef.sum(axis=1).truncate_msb(tapxcoef.bw)

        if self.debug_flag == 2:
            self.debug_data = tapxcoef, tapxcoefsum

        # In the design numbers get truncated by 1 position after each addition,
        # but it does not matter since we are going to chop off 8 digits later anyway

        # Result is scaled down by 2 by adjusting the point positions before rounding; data is not changing

        # For some reason adders do not increase output bit width, supposedly truncating frm the left
        # Finally, output is converted to the specified output type by truncating + rounding
        if self.quantization == "inf":
            dataout = tapxcoefsum.round_from_zero(self.bwout)
        elif self.quantization == "even":
            dataout = tapxcoefsum.round_to_even(self.bwout)
        elif self.quantization == "truncate":
            dataout = tapxcoefsum.truncate(self.bwout)
        else:
            raise ValueError(f"Quantization '{self.quantization}' not implemented")

        if self.debug_flag == 3:
            self.debug_data = tapxcoefsum, dataout

        self.tc_count = (self.tc_count + 1) % self.tapsize
        assert dataout.shape == bdatain.shape, "Out data does not match input shape. Check the algorithm"
        self.bdataout = dataout.bdata

    def coef_gen_calc(self, input_ind: int, tap_ind: int, fwidth: int = 1) -> np.ndarray:
        """
        Reproduces PFB coefficients from the Simulink CASPER model.

        :param input_ind: Which input stream to calculate (of the parallel n_inputs)
        :param tap_ind: Index of the tap to calculate (starting from 0; passing less than 0 will return all coefficients)
        :param fwidth: The scaling of the bin width (1 is normal)
        :return: PFB coefficients for given parameters
        """
        all_taps = self.ntaps * 2 ** self.logsize

        if tap_ind < 0:
            index = np.arange(all_taps)
        else:
            cs = (tap_ind * 2 ** self.logsize) + input_ind
            ce = (tap_ind * 2 ** self.logsize) + 2 ** self.logsize
            step = 2 ** self.logninputs
            index = np.arange(cs, ce, step)

        wval = self.window(all_taps).astype(np.double)
        total_coefs = wval * np.sinc(
            fwidth * ((np.arange(all_taps) + 0.5) / 2 ** self.logsize - self.ntaps / 2).astype(np.double))
        return total_coefs[index]
