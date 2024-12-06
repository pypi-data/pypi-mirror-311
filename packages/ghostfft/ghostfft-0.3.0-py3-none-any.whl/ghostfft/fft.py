import numpy as np
import psutil

from .component import Component
from .fp import FixedPoint, bit_reverse

process = psutil.Process()


def reshape_r2(datafpt: FixedPoint, stage: int):
    shape = datafpt.shape
    datafpt_view = datafpt.reshape(shape[:-1] + (2 ** stage, -1))
    topfpt = datafpt_view[..., 0::2, :].reshape(shape[:-1] + (-1,)).squeeze()
    botfpt = datafpt_view[..., 1::2, :].reshape(shape[:-1] + (-1,)).squeeze()
    return topfpt, botfpt


def unreshape_r2(topfpt: FixedPoint, botfpt: FixedPoint, stage: int):
    shape = topfpt.shape
    nfreq = shape[-1] * 2
    bdata_shape = shape[:-1] + (2 ** stage, shape[-1] * 2 // (2 ** stage))
    datafpt = topfpt.empty(bdata_shape)
    new_shape = shape[:-1] + (-1, bdata_shape[-1])
    datafpt[..., 0::2, :] = topfpt.reshape(new_shape)
    datafpt[..., 1::2, :] = botfpt.reshape(new_shape)
    datafpt.reshape(shape[:-1] + (nfreq,), inplace=True)
    return datafpt


class FFT(Component):
    """
    Stage counting starts from 1
    """

    def __init__(self, logsize: int, logninputs: int, shift_schedule: str, bwin: int = 18, bwout: int = 18,
                 bwcoef: int = 18):
        super().__init__(bwin, bwout)
        self.bwcoef = bwcoef
        self.logsize = logsize
        self.logninputs = logninputs
        if len(shift_schedule) != self.logsize:
            raise ValueError(f"Invalid shift schedule. Expected string of length {self.logsize}")
        self.shift_schedule = np.array([shift_ == '1' for shift_ in shift_schedule])

        self.logger.info(
            f"Initializing {self.__class__.__name__} core with logsize={logsize}, "
            f"logninputs={logninputs}, shift_schedule={shift_schedule}")

        self.binput_buffer = np.zeros(2 ** self.logsize, dtype=np.int32)
        self.boutput_buffer = np.zeros(2 ** self.logsize, dtype=np.int32)
        self.buffer_counter = 0

    def _impl(self, bdatain: np.ndarray = None, **kwargs):
        ind1 = 2 ** self.logninputs * self.buffer_counter
        ind2 = ind1 + 2 ** self.logninputs
        self.bdataout = self.boutput_buffer[ind1:ind2]
        self.binput_buffer[ind1:ind2] = bdatain[:]
        self.buffer_counter += 1

        if self.buffer_counter == 2 ** (self.logsize - self.logninputs):
            self.buffer_counter = 0
            fft_real, fft_imag = self.fft()
            import matplotlib.pyplot as plt
            # plt.plot(self.binput_buffer)
            # plt.plot(fft_real.bdata)
            # plt.plot(fft_imag.bdata)
            # plt.show()
            self.boutput_buffer[0::2] = fft_real[2 ** (self.logsize - 1):]
            self.boutput_buffer[1::2] = fft_imag[2 ** (self.logsize - 1):]

    def twiddle_coef(self, stage: int):
        ind = np.arange(2 ** (self.logsize - 1), dtype=np.int32)
        ind = bit_reverse(ind >> (self.logsize - stage), stage - 1)
        theta = -np.pi * FixedPoint(stage, stage - 1).to_float(ind)
        tw_real = np.cos(theta)
        tw_imag = np.sin(theta)
        mx = (2 ** (self.bwcoef - 1) - 1) / 2 ** (self.bwcoef - 1)
        tw_real = FixedPoint(self.bwcoef, self.bwcoef - 1, tw_real.clip(-mx, mx))
        tw_imag = FixedPoint(self.bwcoef, self.bwcoef - 1, tw_imag.clip(-mx, mx))
        return tw_real, tw_imag

    def butterfly(self, dreal: FixedPoint, dimag: FixedPoint, stage: int):
        top_real, bot_real = reshape_r2(dreal, stage)
        top_imag, bot_imag = reshape_r2(dimag, stage)
        tw_real, tw_imag = self.twiddle_coef(stage)
        print(dreal.bdata, top_real.bdata, tw_real.bdata, stage)
        # fptype_btw = fptype_in * fptype_tw  # promote fptype for tw product
        # fptype_btw = fptype_btw + fptype_btw  # promote fptype for tw sum
        btw_real = bot_real * tw_real - bot_imag * tw_imag
        btw_imag = bot_imag * tw_real + bot_real * tw_imag
        print(btw_real.bdata, btw_imag.bdata, stage)
        print(btw_real.data, btw_imag.data, stage)

        tbtw_real = top_real + btw_real
        tbtw_imag = top_imag + btw_imag
        bbtw_real = top_real - btw_real
        bbtw_imag = top_imag - btw_imag

        print(tbtw_real.bdata, tbtw_imag.bdata, stage)
        print(tbtw_real.data, tbtw_imag.data, stage)
        out_real = unreshape_r2(tbtw_real, bbtw_real, stage)
        out_imag = unreshape_r2(tbtw_imag, bbtw_imag, stage)

        if self.shift_schedule[stage - 1]:
            out_real.downshift(1, inplace=True)
            out_imag.downshift(1, inplace=True)
        # TODO: check if using rounding
        out_real = out_real.reinterpret(self.bwout, self.bwout - 1)
        out_imag = out_imag.reinterpret(self.bwout, self.bwout - 1)
        # print(out_real.conf)
        # out_real = out_real.round_to_even(self.bwout)
        # print(out_real.conf)
        # out_imag = out_imag.round_to_even(self.bwout)
        print(out_real.bdata, out_imag.bdata)
        print("=================")
        return out_real, out_imag

    def fft(self):
        input_data = FixedPoint(self.bwin, self.bwin - 1, self.binput_buffer, disbin=True)
        dreal = input_data.copy()
        dimag = input_data.copy(input_data.bdata * 0)
        # dimag = input_data.copy()

        for stage in range(self.logsize):
            import matplotlib.pyplot as plt
            plt.plot(dreal.bdata)
            plt.plot(dimag.bdata)
            plt.title(str(stage))
            # plt.plot(fft_real.bdata)
            # plt.plot(fft_imag.bdata)
            plt.show()
            dreal, dimag = self.butterfly(dreal, dimag, stage + 1)

        unscramble = bit_reverse(np.arange(2 ** self.logsize), self.logsize)
        return dreal[..., unscramble], dimag[..., unscramble]
