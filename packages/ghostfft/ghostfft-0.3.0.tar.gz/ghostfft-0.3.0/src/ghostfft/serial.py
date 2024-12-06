from typing import List

import numpy as np
from tqdm import tqdm

from .component import Component
from .fp import FixedPoint
from .generators import Generator
from .utils import get_logger


class Serial:
    """
    Currently the only way to program a chain of Components. Implements a sequential design with a single data flow
    without forking. The general puprose is to run controlled loop of steps on each of the connected elements.

    :param generator: The generator to be used as a data source.
    :param components: List of components to be connected sequentially. Does not include the generator.
    :param fpt_out: Output fixed point type. Used for auto calculation of the float data from binary output. If None,
                    the binary data will be written to output.
    """

    def __init__(self, generator: Generator, components: List[Component] | None = None, fpt_out: FixedPoint = None):
        self.components = components

        self.generator = generator
        self.fpt_out = fpt_out
        self.logger = get_logger(self.__class__.__name__)

        if components is None or len(components) == 0:
            self.first_node = None
            self.last_node = generator

        else:
            self.first_node = components[0]
            self.last_node = components[-1]

            for i in range(1, len(self.components)):
                self.components[-i - 1].connect(components[-i])

            if self.generator:
                self.generator.connect(self.first_node)

        if fpt_out is not None and fpt_out.bw != self.last_node.bwout:
            raise ValueError("Specified fpt output does not match last node's output bit width")

    def run(self, clocks: int, pb: bool = True) -> np.ndarray:
        """
        Run the simulation.

        :param clocks: Number of clocks to run the simulation with. Must be a multiple of number of generator outputs.
        :param pb: If True, the progressbar will appear (default True).
        :return: The result data sequence of the simulation.
        """
        if not self.generator:
            raise RuntimeError(f"{self.__class__.__name__}.generator is not specified")
        output = list()

        if clocks % self.generator.nout != 0:
            raise ValueError(
                f"The number of simulation clocks must be a multiple of number of generator outputs {self.generator.nout}.")

        for i in tqdm(range(clocks), disable=not pb):
            self.logger.debug(f"--- {self.__class__.__name__}.run() cycle [{i + 1}/{clocks}] ---")
            self.generator.step()
            if self.fpt_out is not None:
                output.append(
                    self.fpt_out.to_float(self.last_node.bdataout)
                )
            else:
                output.append(self.last_node.bdataout)
        return np.asarray(output)


