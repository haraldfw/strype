import pyaudio


class Audio:
    _stream = None
    _config = None

    _format = pyaudio.paInt16

    def __init__(self, config):
        self._config = config
        self._pyaud = pyaudio.PyAudio()
        self._stream = self._pyaud.open(format=self._format,
                                        channels=config.channels,
                                        rate=config.rate,
                                        input=True,
                                        frames_per_buffer=4 * config.nfft,
                                        input_device_index=config.audio_device)
        self.max_y = 2.0 ** (self._pyaud.get_sample_size(self._format) * 8 - 1)

    def read(self):
        n = int(max(self._stream.get_read_available() / self._config.nfft, 1) * self._config.nfft)
        return self._stream.read(n), n

    def close(self):
        self._stream.stop_stream()
        self._stream.close()
        self._pyaud.terminate()
