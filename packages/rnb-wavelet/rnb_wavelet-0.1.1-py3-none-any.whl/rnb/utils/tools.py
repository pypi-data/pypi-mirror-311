import numpy as np
import math

def compute_spectre_brute(data_epocs, fs):

    if data_epocs.ndim == 1:
        data_epocs = data_epocs[np.newaxis, :]
            
    n_epochs, Ntime = data_epocs.shape

    freq = fs / 2 * np.linspace(0, 1, Ntime // 2 + 1)
    F = np.fft.fft(data_epocs) / Ntime
    F = F[:, :Ntime // 2 + 1]
    F = np.abs(F) ** 2
    # Delete null frequency
    F = F[:, 1:]
    freq = freq[:, 1:]

    if n_epochs > 1:
        F = np.mean(F, axis=0, keepdims=True)

    return freq, F