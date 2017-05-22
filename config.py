import json


def read_config():
    with open('config.json') as f:
        return json.loads(f.read())


class Config:
    audio_device = -1

    def __init__(self):
        c = read_config()
        self.audio_device = c.get('audio-device', 0)
