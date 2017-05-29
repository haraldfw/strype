import atexit
import json
import threading


def read_config():
    with open('config.json') as f:
        return json.loads(f.read())


class Config:
    def __init__(self, c=None):
        if not c:
            c = read_config()
            self._scheduler = Scheduler(self.update)
        self.audio_device = c['audio-device']
        self.channels = c['channels']
        self.rate = c['rate']
        self.bars = c['bars']
        self.leds_per_bar = c['leds_per_bar']
        self.spacer_leds = c['spacer_leds']
        self.chunk_size = c['chunk_size']
        self.min_frequency = c['min_frequency']
        self.max_frequency = c['max_frequency']
        self.decay = c['decay']
        self.colors = ColorConfig(c['color_modes'])
        self.active_color_mode = c['active_color_mode']
        self.tick_per_led = c['tick_per_led']
        self.config_update_interval = c['config_update_interval']

    def update(self):
        c = read_config()
        self.__init__(c)
        self.colors.__init__(c['color_modes'])
        print('Config updated')
        return self

    def start_scheduled_updates(self):
        self._scheduler.run()


class ColorConfig:
    def __init__(self, c):
        self.static = c['static']
        self.fade = c['fade']
        self.rainbow = RainbowConfig(c['rainbow'])


class RainbowConfig:
    def __init__(self, c):
        self.rate = c['rate']
        self.lightness = c['lightness']
        self.saturation = c['saturation']


class Scheduler:
    def __init__(self, update_config):
        self.update_config = update_config
        self._running = True

    def run(self):
        config = self.update_config()
        if self._running:
            threading.Timer(config.config_update_interval, self.run).start()

    @atexit.register
    def stop(self):
        self._running = False
