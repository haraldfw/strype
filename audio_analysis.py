import numpy as np


class Analyzer:
    
    def __init__(self, bars, rate, chunk_size, min_frequency, max_frequency):
        self._rate = rate
        self._min_frequency = min_frequency
        self._chunk_size = chunk_size
        self._max_frequency = max_frequency
        self._bars = bars
        self._frequency_limits = self.calculate_channel_frequencies()

    def analyze(self, data):
        """
        Code inspired by:
         https://github.com/sethshill/sdp/blob/master/synchronized_lights_led_strip.py
        """
        data_stereo = np.fromstring(data, dtype=np.int16)
        data = np.empty(len(data) // 4)  # data has two channels and 2 bytes per channel
        data[:] = data_stereo[::2]  # pull out the even values, just using one channel

        window = np.hanning(len(data))
        data = data * window

        # Apply FFT - real data
        fourier = np.fft.rfft(data)

        # Remove last element in array to make it the same size as chunk size
        fourier = np.delete(fourier, len(fourier) - 1)

        power = np.power(np.abs(fourier), 2)

        matrix = np.zeros(self._bars, dtype=np.float16)
        for i in range(self._bars):
            # take the log10 of the resulting sum to approximate human hearing
            p1 = self.piff(self._frequency_limits[i][0], self._rate)
            p2 = self.piff(self._frequency_limits[i][1], self._rate)
            sums = np.sum(power[p1:p2:1])
            matrix[i] = np.log10(sums)

        return matrix

    def piff(self, val, sample_rate):
        return int(float(self._chunk_size) * val / sample_rate)

    def calculate_channel_frequencies(self):
        """
        Code inspired by:
         https://github.com/sethshill/sdp/blob/master/synchronized_lights_led_strip.py
        """

        bars = self._bars
        min_frequency = self._min_frequency
        max_frequency = self._max_frequency

        print("Calculating frequencies for %d channels." % bars)
        octaves = (np.log(max_frequency / min_frequency)) / np.log(2)
        print("octaves in selected frequency range ... %s" % octaves)
        octaves_per_channel = octaves / bars
        frequency_limits = []
        frequency_store = []

        frequency_limits.append(min_frequency)
        for i in range(1, bars + 1):
            frequency_limits.append(frequency_limits[-1] * 2 ** octaves_per_channel)

        for i in range(0, bars):
            f1 = frequency_limits[i]
            f2 = frequency_limits[i + 1]
            frequency_store.append((f1, f2))
            print("channel %d is %6.2f to %6.2f " % (i, f1, f2))

        return frequency_store
