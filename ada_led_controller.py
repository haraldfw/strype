import Adafruit_WS2801
import math

from Adafruit_GPIO import SPI

_led_count = 160
_leds = None
_spacer_length = -1
_bar_length = -1
_bar_amount = -1

col_static_r = 255
col_static_g = 255
col_static_b = 255


bar_indexes = []


def init(led_count, bar_amount, bar_length, spacer_length, col_cfg):
    global _led_count, _leds, _spacer_length, _bar_length, _bar_amount, col_static_r, col_static_g, col_static_b, \
        color_func, bar_indexes
    _led_count = led_count

    _leds = Adafruit_WS2801.WS2801Pixels(led_count, spi=SPI.SpiDev(0, 0))

    _leds.clear()
    _leds.show()

    _spacer_length = spacer_length
    _bar_length = bar_length
    _bar_amount = bar_amount

    col_static_r = col_cfg['modes']['static']['r']
    col_static_g = col_cfg['modes']['static']['g']
    col_static_b = col_cfg['modes']['static']['b']

    color_func = get_static_color

    bar_indexes = []
    shift_indexes = []
    flip = False
    shift = 0
    for b in range(bar_amount):
        ixs = [i + shift for i in range(bar_length)]
        shift += _bar_length + _spacer_length
        if flip:
            ixs = [i for i in reversed(ixs)]
        bar_indexes.append(ixs)
        flip = not flip
    # print(bar_indexes)


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

    for i, bar in enumerate(bar_indexes):
        height = heights[i] * _bar_length
        for j, k in enumerate(bar):
            if j < height:
                set_led_rgb(k)
    show()
