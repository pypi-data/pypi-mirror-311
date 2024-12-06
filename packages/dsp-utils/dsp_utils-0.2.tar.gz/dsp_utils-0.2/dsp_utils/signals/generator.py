from dataclasses import dataclass
import numpy as np
from collections.abc import Iterable
from scipy import signal


########################################################################
@dataclass
class SignalGenerator:
    frequency: float
    amplitude: float
    duration: float
    sampling_rate: float
    phase: float = 0
    time_endpoint: bool = False

    # ----------------------------------------------------------------------
    def __post_init__(self):
        """"""
        n = self.duration * self.sampling_rate

        if isinstance(self.frequency, Iterable):
            frequency = []
            for f in self.frequency:
                if isinstance(f, Iterable):
                    frequency.append(np.linspace(f[0], f[1], n))
                else:
                    frequency.append(np.array([f] * n))
            self.frequency = np.array(frequency)

        if isinstance(self.amplitude, Iterable):
            self.amplitude = np.array(self.amplitude)[:, np.newaxis]

    # ----------------------------------------------------------------------
    @property
    def time(self):
        """"""
        return np.linspace(
            0,
            self.duration,
            self.duration * self.sampling_rate,
            endpoint=self.time_endpoint,
        )

    # ----------------------------------------------------------------------
    @property
    def time_tile(self):
        """"""
        if isinstance(self.frequency, np.ndarray):
            return np.tile(self.time, (self.frequency.shape[0], 1))
        else:
            return self.time

    # ----------------------------------------------------------------------
    @property
    def sine_wave(self):
        """"""
        return self.amplitude * np.sin(
            2 * np.pi * self.frequency * self.time_tile + self.phase
        )

    # ----------------------------------------------------------------------
    @property
    def square_wave(self):
        """"""
        return self.amplitude * signal.square(
            2 * np.pi * self.frequency * self.time_tile + self.phase
        )

    # ----------------------------------------------------------------------
    @property
    def triangle_wave(self):
        """"""
        return self.amplitude * signal.sawtooth(
            2 * np.pi * self.frequency * self.time_tile + self.phase, width=0.5
        )

    # ----------------------------------------------------------------------
    @property
    def sawtooth_wave(self):
        """"""
        return self.amplitude * signal.sawtooth(
            2 * np.pi * self.frequency * self.time_tile + self.phase, width=1
        )

    # ----------------------------------------------------------------------
    def gaussian_noise(self, /, mean=0, std_dev=0.5):
        """"""
        return np.random.normal(mean, std_dev, self.time_tile.shape)

    # ----------------------------------------------------------------------
    def power(self, time_series):
        """"""
        return np.mean(time_series**2)

    # ----------------------------------------------------------------------
    def gaussian_noise_db(self, time_series, /, db=3):
        """"""
        signal_power = self.power(time_series)
        snr_linear = 10 ** (db / 10)
        noise_power = signal_power / snr_linear

        return np.random.normal(0, np.sqrt(noise_power), time_series.shape)
