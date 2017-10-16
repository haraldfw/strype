import pyaudio


class Audio:
    _stream = None

    _format = pyaudio.paInt16

    def __init__(self, channels, rate, chunk_size, audio_device_index):
        self._chunk_size = chunk_size
        self._pyaud = pyaudio.PyAudio()
        self._stream = self._pyaud.open(format=self._format,
                                        channels=channels,
                                        rate=rate,
                                        input=True,
                                        frames_per_buffer=chunk_size,
                                        input_device_index=audio_device_index)
        self.max_y = 2.0 ** (self._pyaud.get_sample_size(self._format) * 8 - 1)

    def read(self):
        data = self._stream.read(self._chunk_size, exception_on_overflow=False)
        # print(data)
        return data

    def close(self):
        self._stream.stop_stream()
        self._stream.close()
        self._pyaud.terminate()
