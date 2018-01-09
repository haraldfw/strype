import numpy
from logzero import logger

import ws281x_driver as driver

_led_count = 160
_leds = None  # type: driver
_spacer_length = -1
_bar_length = -1
_bar_amount = -1

col_static_r = 255
col_static_g = 255
col_static_b = 255

bar_indexes = []
spacer_indexes = []


def init(led_count, bar_amount, bar_length, spacer_length, led_cfg, col_cfg):
    global _led_count, _leds, _spacer_length, _bar_length, _bar_amount, col_static_r, col_static_g, col_static_b, \
        color_func, bar_indexes, spacer_indexes
    _led_count = led_count

    driver.init(led_count, 0)
    _leds = driver

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
    spacer_indexes = []
    flip = led_cfg['flip']
    shift = 0
    for b in range(bar_amount):
        ixs = [i + shift for i in range(bar_length)]
        sixs = [shift + i + bar_length for i in range(spacer_length)]
        shift += _bar_length + _spacer_length
        if flip:
            ixs = [i for i in reversed(ixs)]
        bar_indexes.append(ixs)
        spacer_indexes.append(sixs)
        flip = not flip

    logger.debug(bar_indexes)
    logger.debug(spacer_indexes)


def get_static_color():
    return col_static_r, col_static_g, col_static_b


color_func = get_static_color


def set_led(n, invert=False, rotate=False, scale=1):
    c = color_func()
    if invert:
        c = [255 - c[0], 255 - c[1], 255 - c[2]]
    if rotate:
        c = c[1:] + c[:1]

    c = [int(r * scale) for r in c]

    _leds.set_color(n, c[0], c[1], c[2])


def show():
    _leds.show()


def clear():
    _leds.clear()


def _update_spacers(heights):
    fourths = _bar_amount // 4
    invert = numpy.average(heights[:fourths]) > 0.8
    rotate = numpy.average(heights[_bar_amount - fourths:]) > 0.65

    if invert and rotate:
        half = _bar_amount // 2
        for i in spacer_indexes[:half]:
            for j in i:
                set_led(j, invert=invert)

        for i in spacer_indexes[half:]:
            for j in i:
                set_led(j, rotate=rotate)

    elif invert or rotate:
        for i in spacer_indexes:
            for j in i:
                set_led(j, invert=invert, rotate=rotate)


def _update_spacers2(spacers):
    half = _bar_amount // 2

    for ixs in spacer_indexes[:half]:
        for i in ixs:
            set_led(i, invert=True, scale=spacers[1])

    for ixs in spacer_indexes[half:]:
        for i in ixs:
            set_led(i, rotate=True, scale=spacers[0])


def update(heights, spacers):
    clear()
    if _spacer_length:
        _update_spacers2(spacers)

    for i, bar in enumerate(bar_indexes):
        height = heights[i] * _bar_length
        for j, k in enumerate(bar):
            if j < height:
                set_led(k)
    show()
