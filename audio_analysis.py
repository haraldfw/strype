import struct

import numpy as np


class Analyzer:
    _config = None
    buffsize = -1

    def __init__(self, config):
        self._config = config
        self.buffsize = 4 * config.nfft

    def parse(self, max_y, data, n):
        y = np.array(struct.unpack("%dh" % (n * self._config.channels), data)) / max_y
        y = y.flatten()

        left, right = np.split(np.abs(np.fft.fft(y)), 2)
        ys = np.add(left, right[::-1])
        ys = np.multiply(20, np.log10(ys))
        ys = np.clip(ys, a_min=0, a_max=100000000)
        xs = np.arange(self.buffsize, dtype=float)

        j = self.buffsize
        ys = ys[:j]
        xs = xs[:j] * self._config.rate / self.buffsize
        # ys = np.divide(100, ys)
        ys = ys / 100.0

        return ys
