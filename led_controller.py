import numpy
from logzero import logger

import ws281x_driver as driver

import colors.color_controller as color

_led_count = 160
_leds = None  # type: driver
_spacer_length = -1
_bar_length = -1
_bar_amount = -1

col_static_r = 255
col_static_g = 255
col_static_b = 255

bar_indices = []
spacer_indices = []


def init(cfg):
    global _led_count, _leds, _spacer_length, _bar_length, _bar_amount, col_static_r, col_static_g, col_static_b, \
        bar_indices, spacer_indices
    led_cfg = cfg['led']
    led_count = led_cfg['amount']
    bar_amount = led_cfg['bar-amount']
    bar_length = led_cfg['bar-length']
    spacer_length = led_cfg['spacer-length']

    _led_count = led_count

    driver.init(led_count, 0)
    _leds = driver

    _leds.clear()
    _leds.show()

    _spacer_length = spacer_length
    _bar_length = bar_length
    _bar_amount = bar_amount

    color.init(cfg)

    bar_indices = []
    spacer_indices = []
    flip = led_cfg['flip']
    shift = 0
    for b in range(bar_amount):
        ixs = [i + shift for i in range(bar_length)]
        sixs = [shift + i + bar_length for i in range(spacer_length)]
        shift += _bar_length + _spacer_length
        if flip:
            ixs = [i for i in reversed(ixs)]
        bar_indices.append(ixs)
        spacer_indices.append(sixs)
        flip = not flip

    logger.debug(bar_indices)
    logger.debug(spacer_indices)


def set_led(n, height):
    c = color.get_color(n, height)
    _leds.set_color(n, c[0], c[1], c[2])


def show():
    _leds.show()


def clear():
    _leds.clear()


def update(heights, spacers):
    clear()
    for i, bar in enumerate(bar_indices):
        height = heights[i] * _bar_length
        color.height_update(height)
        for j, k in enumerate(bar):
            if j < height:
                color.i_update(k, height)
                set_led(k, height)
    show()
