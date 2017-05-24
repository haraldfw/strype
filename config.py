import json


def read_config():
    with open('config.json') as f:
        return json.loads(f.read())


class Config:
    audio_device = -1

    def __init__(self):
        c = read_config()
        self.audio_device = c.get('audio-device', 0)
        self.nfft = c.get('nfft', 0)
        self.channels = c.get('channels', 0)
        self.rate = c.get('rate', 0)
