import numpy as np

from .component import Component
from .fp import FixedPoint


class Generator(Component):
    """
    An abstract class representing a generator component. The generators must be present in any
    component chain at the beginning, as they are the entry point of any data and also time trackers.

    :param lognout: Log number of parallel outputs. This slows down the clock, as 2**lognout sequential
                    points from the simulated ADC input are sent to output in parallel. For example, if
                    specified sample rate is 800 Msps and lognout is 2, then the effective clock at the output
                    will be 200 MHz.
    :param sample_rate: Sample rate of the simulated ADC in [Msps].
    :param bwout: Bit width of the output data.
    :param clock_loop: Integer number of clocks that will be looped.
    """

    def __init__(self, lognout: int, sample_rate: float, bwout: int, clock_loop: int = None, **kwargs):
        super().__init__(bwin=None, bwout=bwout, **kwargs)
        f"Initializing {self.__class__.__name__} with sample_rate={sample_rate} Msps, lognout={lognout}"
        self.nout = 2 ** lognout
        self.bwout = bwout

        # Clock is an integer step number, but generators take real time as an input in [s]
        self.clock: int = 0
        # Real time for each step which includes 2**lognout points
        self.t: np.ndarray = np.zeros(self.nout)
        self.delta_t: float = 1 / sample_rate / 1e6
        self.clock_loop = clock_loop

    def step(self, bdatain=None, **kwargs):
        """
        Overrides the default Component.step() to enable clock tracking.

        :param bdatain: Data array to be processed. Usually not applicable to generators.
        :param kwargs: Additional keyword arguments that will be passed to the _impl().
        """
        clock_step = np.arange(self.nout) + self.clock

        if self.clock_loop:
            clock_step = clock_step % self.clock_loop

        self.t = clock_step * self.delta_t

        self.clock += self.nout
        self.logger.debug(f"Increasing clock to {self.clock}")
        self.logger.debug(f"New timestamps for generator step are {self.t}")
        super(Generator, self).step(bdatain, **kwargs)


class SinGenerator(Generator):
    """
    Generates integer sinusoidal data.

    :param lognout: Log number of parallel outputs
    :param sample_rate: Sample rate of the simulated ADC in [Msps]
    :param bwout: Bit width of the output data
    :param freq: Frequency of the sinusoid in [MHz]
    :param ampl: Integer amplitude of the sinusoid; will be truncated if does not fit into bwout
    """

    def __init__(self, lognout: int, sample_rate: float, bwout: int, freq: float, ampl: int, clock_loop: int = None,
                 **kwargs):
        super().__init__(lognout, sample_rate, bwout, clock_loop, **kwargs)
        self.logger.debug(f"{self.__class__.__name__} ampl={ampl}, freq={freq} MHz")
        self.ampl = ampl
        self.freq = freq

    def _impl(self, bdatain: np.ndarray = None, **kwargs):
        data = np.sin(2 * np.pi * self.freq * 1e6 * self.t) * self.ampl
        self.bdataout = FixedPoint(self.bwout, 0, data).bdata


class ConstGenerator(Generator):
    """
    Generates constant integer data.

    :param lognout: Log number of parallel outputs
    :param sample_rate: Sample rate of the simulated ADC in [Msps]
    :param bwout: Bit width of the output data
    :param freq: Frequency of the sinusoid in [MHz]
    :param ampl: Integer amplitude of the sinusoid; will be truncated if does not fit into bwout
    """

    def __init__(self, lognout: int, sample_rate: float, bwout: int, ampl: int, clock_loop: int = None, **kwargs):
        super().__init__(lognout, sample_rate, bwout, clock_loop, **kwargs)
        self.logger.debug(f"{self.__class__.__name__} ampl={ampl}")
        self.ampl = ampl

    def _impl(self, bdatain: np.ndarray = None, **kwargs):
        self.bdataout = FixedPoint(self.bwout, 0, np.full(self.nout, self.ampl)).bdata


class NoiseGenerator(Generator):
    """
    To be implemented.
    """


class DataGenerator(Generator):
    """
    To be implemented.
    """
