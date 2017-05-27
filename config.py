import json


def read_config():
    with open('config.json') as f:
        return json.loads(f.read())


class Config:
    audio_device = -1
    channels = -1
    rate = -1
    bars = -1
    chunk_size = -1
    min_frequency = -1
    max_frequency = -1
    decay = -1

    def __init__(self):
        c = read_config()
        self.audio_device = c.get('audio-device', 0)
        self.channels = c.get('channels', 0)
        self.rate = c.get('rate', 0)
        self.bars = c.get('bars', 0)
        self.chunk_size = c.get('chunk_size', 0)
        self.min_frequency = c.get('min_frequency')
        self.max_frequency = c.get('max_frequency')
        self.decay = c.get('decay')
