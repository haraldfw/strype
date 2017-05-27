import pyaudio


class Audio:
    _stream = None
    _config = None

    _format = pyaudio.paInt16

    def __init__(self, config):
        """
         :type config: config.Config
        """
        self._config = config
        self._pyaud = pyaudio.PyAudio()
        self._stream = self._pyaud.open(format=self._format,
                                        channels=config.channels,
                                        rate=config.rate,
                                        input=True,
                                        frames_per_buffer=config.chunk_size,
                                        input_device_index=config.audio_device)
        self.max_y = 2.0 ** (self._pyaud.get_sample_size(self._format) * 8 - 1)

    def read(self):
        data = self._stream.read(self._config.chunk_size)
        return data

    def close(self):
        self._stream.stop_stream()
        self._stream.close()
        self._pyaud.terminate()
