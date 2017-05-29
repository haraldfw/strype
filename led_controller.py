import colorsys

import Adafruit_WS2801
import RPi.GPIO as GPIO
from Adafruit_GPIO import SPI


def parse_colors(config):
    modes = {}


class LEDController:
    def __init__(self, config, func):
        """
         :type config: config.Config
        """
        self._colorer = LedColorer(config)
        self._config = config
        self._get_data = func
        self._color = 0
        self._col_starts = None
        self._pixels = None
        self._pixels = Adafruit_WS2801.WS2801Pixels(
            (self._config.leds_per_bar + self._config.spacer_leds) * self._config.bars,
            spi=SPI.SpiDev(0, 0), gpio=GPIO)
        self._col_starts = []
        for i in range(len(self._config.bars)):
            self._col_starts.append(i * (self._config.leds_per_bar + self._config.spacer_leds))

    def start(self):
        print('LEDController started')
        self._pixels.clear()
        while True:
            heights = self._get_data()
            if self._config.tick_per_time:
                self._colorer.tick()
            for h, c in zip(heights, self._col_starts):
                self.display_column(h, c)
            self._pixels.show()

    def display_column(self, height, col_start):
        # column
        if self._config.tick_per_column:
            self._colorer.tick()
        for i in range(self._config.leds_per_bar):
            # led
            if self._config.tick_per_led:
                self._colorer.tick()
            if i < height:
                self.led_on(col_start + i)
            else:
                self.led_off(col_start + i)

    def led_on(self, index):
        self._pixels.set_pixel_rgb(index, self._colorer.r, self._colorer.g, self._colorer.b)

    def led_off(self, index):
        self._pixels.set_pixel_rgb(index, 0, 0, 0)


class LedColorer:
    def __init__(self, config):
        """
         :type config: config.Config
        """
        self._config = config
        cm = config.active_color_mode
        if cm == 'static':
            self._color_func = self._static
            self.r, self.g, self.b = self._config.colors.static
        elif cm == 'rainbow':
            self._color_func = self._rainbow
            self.hue = 0.0
        elif cm == 'fade':
            self._color_func = self._fade
        else:
            raise ValueError('Invalid colormode \'' + cm + '\'')

        self.r, self.g, self.b = self._config.colors.static
        self.tick()

    def _static(self):
        pass

    def _rainbow(self):
        self.r, self.g, self.b = [c * 255 for c in colorsys.hls_to_rgb(
            self.hue,
            self._config.colors.rainbow.lightness,
            self._config.colors.rainbow.saturation)]
        self.hue += self._config.colors.rainbow.rate
        if self.hue > 359:
            self.hue -= 359

    def _fade(self):
        pass

    def tick(self):
        self._color_func()
