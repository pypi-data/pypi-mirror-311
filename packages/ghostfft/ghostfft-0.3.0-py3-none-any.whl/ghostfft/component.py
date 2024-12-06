import os.path

import numpy as np

from .utils import get_logger


class Component:
    """
    Base class for simulating component models. Implements basic operations like logging, processing pipeline, etc.

    The input and output bit width must be specified. The shape of the data array can be any.

    All child classes must implement the Component._impl() method that takes bdatain as an input and writes the output to the
    self.bdataout

    :bwin: The bit width of the input data array.
    :bwout: The bit width of the output data array.
    :datalog: If True, the component data output is logged.
    """

    def __init__(self, bwin: int | None, bwout: int, datalog: str = None, **kwargs):
        self.logger = get_logger(self.__class__.__name__)
        self.logger.debug(f"Initializing base for {self.__class__.__name__} with input BW={bwin} and output BW={bwout}")
        self.bwin = bwin
        self.bwout = bwout
        self.bdataout = None
        self.datalog = datalog
        self.datalog_bdata = []

        self.connected = []

    def _impl(self, bdatain: np.ndarray = None, **kwargs):
        """
        A placeholder method that is expected to be overridden by subclasses. Accepts the input at simulation step and
        updates the output data in self.dataout.
        :param bdatain: The input data in binary format to be processed.
        :param kwargs: Extra parameters to configure the behaviour of the component.
        """
        if not self.__class__.__name__ in ["Component", "Generator"]:
            self.logger.warning(f"The core of the {self.__class__.__name__} was not implemented yet. Returning input.")
        self.bdataout = bdatain

    def connect(self, component: "Component"):
        """
        Connect the input of a given Component to the output of this. The data will be passed at the end of step()
        method and the connected component will be called.

        :param component: A Component to be connected.
        """
        if component.bwin != self.bwout:
            raise RuntimeError(f"Cannot connect  components with different port bit widths. {self.__class__.__name__} "
                               f"has output bit width {self.bwout} and {component.__class__.__name__} has input bit "
                               f"width {component.bwin}.")
        self.logger.info(f"Connected output of {self.__class__.__name__} to the input of {component.__class__.__name__}"
                         f" with BW={self.bwout}")
        if component not in self.connected:
            self.connected.append(component)

    def step(self, bdatain: np.ndarray = None, **kwargs):
        """
        Performs a single iteration of the Component logic which corresponds to one clock. Takes bdatain as an input
        and calls the _impl logic.
        :param bdatain: Data array to be processed.
        :param kwargs: Additional keyword arguments that will be passed to the _impl().
        """
        if bdatain is not None:
            bdatain = np.squeeze(bdatain)
            assert isinstance(bdatain, np.ndarray), "bdatain must be a numpy array"
            assert isinstance(bdatain[0], np.integer), "bdatain must be an integer in binary form"

        self._impl(bdatain, **kwargs)

        if self.datalog:
            self.datalog_bdata.append(self.bdataout)

        for conn in self.connected:
            self.logger.debug(f"{self.__class__.__name__} sending data {self.bdataout} to {conn.__class__.__name__}")
            conn.step(self.bdataout)

    def log2mat(self, filename: str = "datalog.mat", overwrite: bool = True):
        """
        If data was logged, exports it to the matalab format that can be read in Simulink.

        :param filename: Path to the matalab file.
        :param overwrite: Overwrite existing matalab file.
        """
        import hdf5storage
        if len(self.datalog_bdata) == 0:
            raise RuntimeError("Data log array is empty. Enable data logging with datalog=True in Component definition")
        data = np.asarray(self.datalog_bdata)
        data_t = np.reshape(data, (len(data), -1)).T
        all_data = np.vstack([np.arange(data_t.shape[1]), data_t]).astype(np.float64)

        data_dict = dict(data=all_data)

        if not filename.endswith(".mat"):
            filename += ".mat"
        if os.path.exists(filename):
            if overwrite:
                os.remove(filename)
            raise FileExistsError(f"File {filename} already exists and overwrite=False")
        hdf5storage.write(data_dict, '.', filename, matlab_compatible=True)
