import json


def read_config():
    with open('config.json') as f:
        return json.loads(f.read())


def read_property(key, default, config_dict):
    try:
        return config_dict[key]
    except KeyError:
        return default


class Config:
    audio_device = -1

    def __init__(self):
        c = read_config()
        self.audio_device = read_property('audio-device', 0, c)
