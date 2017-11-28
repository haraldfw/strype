from numpy import *
from rpi_audio_levels import AudioLevels

_rate = None
_min_frequency = None
_chunk_size = None
_max_frequency = None
_bars = 0
_frequency_limits = None
_audio_levels = None
_piff = None


def init(bars, rate, chunk_size, min_frequency, max_frequency):
    global _rate, _min_frequency, _chunk_size, _max_frequency, _bars, _frequency_limits, _audio_levels, _piff
    _rate = rate
    _min_frequency = min_frequency
    _chunk_size = chunk_size
    _max_frequency = max_frequency
    _bars = bars
    _frequency_limits = calculate_channel_frequencies()
    _audio_levels = AudioLevels(math.log(chunk_size / 2, 2), len(_frequency_limits))

    fl = array(_frequency_limits)
    _piff = ((fl * chunk_size) / _rate).astype(int)
    for a in range(len(_piff)):
        if _piff[a][0] == _piff[a][1]:
            _piff[a][1] += 1
    _piff = _piff.tolist()


def analyze(data):
    """Calculate frequency response for each channel defined in frequency_limits

        :param data: decoder.frames(), audio data for fft calculations
        :type data: decoder.frames

        :return:
        :rtype: numpy.array
        """
    # create a numpy array, taking just the left channel if stereo
    data_stereo = frombuffer(data, dtype=int16)
    data = array(data_stereo[::2])

    # if you take an FFT of a chunk of audio, the edges will look like
    # super high frequency cutoffs. Applying a window tapers the edges
    # of each end of the chunk down to zero.
    window = hanning(len(data)).astype(float32)

    data = data * window

    # if all zeros in data then there is no need to do the fft
    if all(data == 0.0):
        return zeros(len(data), dtype=float32), False

    levels, means, stds = _audio_levels.compute(data, _piff)
    print(levels)
    return levels, True


def calculate_channel_frequencies():
    """
    Code inspired by:
     https://github.com/sethshill/sdp/blob/master/synchronized_lights_led_strip.py
    """

    bars = _bars
    min_frequency = _min_frequency
    max_frequency = _max_frequency

    print("Calculating frequencies for %d channels." % bars)
    octaves = (log(max_frequency / min_frequency)) / log(2)
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
