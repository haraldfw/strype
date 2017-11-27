from __future__ import division

import Adafruit_WS2801
import numpy

_led_count = 160
_leds = None
_spacer_length = -1
_bar_length = -1
_bar_amount = -1


def init(led_count, bar_amount, bar_length, spacer_length, pin_clock=18, pin_dout=23):
    global _led_count, _leds, _spacer_length, _bar_length, _bar_amount
    _led_count = led_count

    _leds = Adafruit_WS2801.WS2801Pixels(led_count, clk=pin_clock, do=pin_dout)

    _leds.clear()
    _leds.show()

    _spacer_length = spacer_length
    _bar_length = bar_length
    _bar_amount = bar_amount


def set_led(coordinate, color):
    _leds.set_pixel(coordinate, color)


def set_led_rgb(n, r, g, b):
    _leds.set_pixel_rgb(n, r, g, b)


def show():
    _leds.show()


def clear():
    _leds.clear()


def update(heights):
    clear()
    # if len(heights) != _bar_amount:
    #     logger.error('CONFIGURATION INCONSISTENCY: Length of given heights array is not equal '
    #                    'to the defined amount of bars. Returning...')
    #     return
    c = numpy.amax(heights)
    c = numpy.floor(c * _led_count)
    # print(c)

    for i in range(numpy.int(c)):
        set_led_rgb(i, 10, 10, 10)
    show()
