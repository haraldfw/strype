from __future__ import division
import time

import math
import numpy
from logzero import logger

import Adafruit_WS2801


class LEDController:
    _led_count = 160
    _leds = None

    def __init__(self, led_count, bar_amount, bar_length, spacer_length, pin_clock=18, pin_dout=23):
        self._led_count = led_count

        self._leds = Adafruit_WS2801.WS2801Pixels(led_count, clk=pin_clock, do=pin_dout)

        self._leds.clear()
        self._leds.show()

        self._spacer_length = spacer_length
        self._bar_length = bar_length
        self._bar_amount = bar_amount

    def set_led(self, coordinate, color):
        self._leds.set_pixel(coordinate, color)

    def set_led_rgb(self, n, r, g, b):
        self._leds.set_pixel_rgb(n, r, g, b)

    def show(self):
        self._leds.show()

    def clear(self):
        self._leds.clear()

    def update(self, heights):
        self.clear()
        # if len(heights) != self._bar_amount:
        #     logger.warning('CONFIGURATION INCONSISTENCY: Length of given heights array is not equal '
        #                    'to the defined amount of bars. Returning...')
        #     return
        c = numpy.amax(heights)
        c = numpy.floor(c * self._led_count)
        print(c)

        for i in range(numpy.int(c)):
            self.set_led_rgb(i, 10, 10, 10)
        self.show()
