import numpy as np
from scipy.signal import butter, filtfilt
from scipy.fftpack import fft, ifft, fftshift, fftfreq
from enum import Enum

from .enums import SignalFilterName, SignalFilterType


def filter_signal(x, lf: float, rf: float, fname: SignalFilterName, ftype: SignalFilterType):
    return x


class Units(Enum):
    ACCELERATION = "Виброускорение, м/c^2"
    VELOCITY = "Виброскорость, мм/с"
    DISPLACEMENT = "Виброперемещение, мкм"

class Window(Enum):
    HANNING = np.hanning
    HAMMING = np.hamming


"""
Функции окна
"""
def apply_window(x, w=None):
    n = len(x)
    f = np.hanning
    if w:
        if w == Window.HAMMING:
            f = np.hamming
    y = f(n) * x
    return y

"""
Функции фильтрации
"""
def bandpass_filter(data, lowcut, highcut, fs, order=4):
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    return filtfilt(b, a, data)


"""
Функции перевода единиц измерения
"""
def accel_to_dB(x):
    return 20 * np.log10(x / 1e-6)

def g_to_accel(x):
    g = 9.81  # м/с^2
    return g * x


"""
Функции обработки сигнала
"""
def signal_to_amp_spectr(x, fs):
    # Вычисление спектра огибающей
    n = len(x)
    frequencies = np.fft.fftfreq(n, d=1/fs)  # Частоты для БПФ
    spectrum = np.fft.fft(x)  # БПФ огибающей
    amp_spectrum = 2 / n * np.abs(spectrum)  # Модуль спектра
    return frequencies[:n//2], amp_spectrum[:n//2]