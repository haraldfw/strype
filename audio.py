import pyaudio
from logzero import logger

import error
from error import StrypeException

_stream = None
_format = pyaudio.paInt16
_chunk_size = -1
_pyaud = None
max_y = -1


def init(channels, rate, chunk_size, audio_device_index):
    global _chunk_size, _pyaud, _stream, max_y
    _chunk_size = chunk_size
    _pyaud = pyaudio.PyAudio()

    if audio_device_index == 'auto' or audio_device_index < 0:
        audio_device_index = get_likely_loopback_index(_pyaud, channels)
    logger.info('Initializing audio stream with index {} and chunk size {}'.format(audio_device_index, chunk_size))
    try:
        _stream = _pyaud.open(format=_format,
                              channels=channels,
                              rate=rate,
                              input=True,
                              frames_per_buffer=chunk_size,
                              input_device_index=audio_device_index)
    except OSError as e:
        raise StrypeException(error.AUDIO_EXCEPTION,
                              'Error caught while creating audio device. Run strype with flag \'-l\' to list devices, '
                              'and edit config accordingly. Error message was: {}'.format(e))
    max_y = 2.0 ** (_pyaud.get_sample_size(_format) * 8 - 1)


def get_likely_loopback_index(pyaud, channels):
    valid_devices = []
    for i in range(pyaud.get_device_count()):
        device = pyaud.get_device_info_by_index(i)
        ic = device['maxInputChannels']
        if int(ic) == int(channels):
            valid_devices.append(device['index'])
    devs_found = len(valid_devices)
    if devs_found != 1:
        raise StrypeException(error.INVALID_AUDIO_INDEX,
                              'Unable to automatically get input-device. {} devices with {} maxInputChannels found. '
                              'Please specify a device index in the config file (audio.device-index) or check '
                              'that any exist with the \'-l\' flag.'.format(devs_found, channels))
    else:
        return valid_devices[0]


def read():
    data = _stream.read(_chunk_size, exception_on_overflow=False)
    return data


def close():
    _stream.stop_stream()
    _stream.close()
    _pyaud.terminate()
