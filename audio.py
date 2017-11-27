import sys

import pyaudio
from logzero import logger

_stream = None
_format = pyaudio.paInt16
_chunk_size = -1
_pyaud = None
max_y = -1


def init(channels, rate, chunk_size, audio_device_index):
    global _chunk_size, _pyaud, _stream, max_y
    logger.info('Initializing audio stream with index {} and chunk size {}'.format(audio_device_index, chunk_size))
    _chunk_size = chunk_size
    _pyaud = pyaudio.PyAudio()
    try:
        _stream = _pyaud.open(format=_format,
                              channels=channels,
                              rate=rate,
                              input=True,
                              frames_per_buffer=chunk_size,
                              input_device_index=audio_device_index)
    except OSError as e:
        logger.error('Error caught while creating audio device. Run strype with flag \'-l\' to list devices, and edit '
                     'config accordingly.\nError message was:\n{}'.format(e))
        sys.exit(1)
    max_y = 2.0 ** (_pyaud.get_sample_size(_format) * 8 - 1)


def read():
    data = _stream.read(_chunk_size, exception_on_overflow=False)
    return data


def close():
    _stream.stop_stream()
    _stream.close()
    _pyaud.terminate()
