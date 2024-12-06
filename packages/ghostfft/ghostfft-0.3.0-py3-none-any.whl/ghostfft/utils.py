import logging
import warnings

import h5py
import numpy as np


def get_logger(name: str):
    ch = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s %(levelname)8s %(name)s | %(message)s')
    ch.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.addHandler(ch)
    return logger


def load_simulink(file_name, arr_name):
    with h5py.File(file_name) as f:
        return f[arr_name][()][:, 1]


# def to_mat_file(fname: str, arr_name: np.ndarray, ninputs: int, args):
#     """
#     Reshapes 1D array and saves it in mat file for input in simulink.
#
#     :param fname:
#     :param arr_name:
#     :return:
#     """
#   TODO: remove this function

#     warnings.warn("The 'estimate_latency' method is deprecated", DeprecationWarning, 2)
#     import hdf5storage
#     frame_size = 16384
#     sample_rate = 3.2e9
#     ninputs = 8
#
#     _frame_duration = 1 / sample_rate * frame_size
#     _sample_duration = 1 / sample_rate
#     _ncycles = args.freq * 1e6 * _frame_duration
#     t = np.arange(args.nframes * frame_size) / sample_rate
#     data = np.sin(args.freq * 1e6 * t * 2 * np.pi) * (args.ampl * 2 ** 13 - 1)
#
#     data_t = np.reshape(data, (-1, ninputs)).T
#     all_data = np.vstack([np.arange(data_t.shape[1]), data_t])
#
#     data_dict = dict(data=all_data)
#     hdf5storage.write(data_dict, ".", args.fname + '.mat', matlab_compatible=True)

def estimate_latency(data_, data_ref):
    # TODO: remove this function
    warnings.warn("The 'estimate_latency' method is deprecated", DeprecationWarning, 2)
    latency = 0
    chi2 = float("inf")
    for i in range(100):
        rdata = np.roll(data_, i)
        rdata[0:i] = 0
        chi2_new = np.sum((data_ref - rdata) ** 2)
        if chi2_new < chi2:
            chi2 = chi2_new
            latency = i
    return latency
