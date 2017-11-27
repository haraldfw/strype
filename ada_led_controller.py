from __future__ import division

import Adafruit_WS2801

_led_count = 160
_leds = None
_spacer_length = -1
_bar_length = -1
_bar_amount = -1

col_static_r = 255
col_static_g = 255
col_static_b = 255


def init(led_count, bar_amount, bar_length, spacer_length, col_cfg, pin_clock=18, pin_dout=23):
    global _led_count, _leds, _spacer_length, _bar_length, _bar_amount, col_static_r, col_static_g, col_static_b, \
        color_func
    _led_count = led_count

    _leds = Adafruit_WS2801.WS2801Pixels(led_count, clk=pin_clock, do=pin_dout)

    _leds.clear()
    _leds.show()

    _spacer_length = spacer_length
    _bar_length = bar_length
    _bar_amount = bar_amount

    col_static_r = col_cfg['modes']['static']['r']
    col_static_g = col_cfg['modes']['static']['g']
    col_static_b = col_cfg['modes']['static']['b']

    color_func = get_static_color


def get_static_color():
    return col_static_r, col_static_g, col_static_b


color_func = get_static_color


def set_led_rgb(n):
    c = color_func()
    _leds.set_pixel_rgb(n, c[0], c[2], c[1])


def show():
    _leds.show()


def clear():
    _leds.clear()


def update(heights):
    clear()

    shift = 0
    for h in heights:
        height = h * _bar_length

        for i in range(_bar_length):
            if i < height:
                set_led_rgb(i + shift)
        shift += _bar_length + _spacer_length

    show()
