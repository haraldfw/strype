from colorsys import hsv_to_rgb

low = -1
high = -1
saturation = -1
value = -1

diff = -1
bar_length = -1
last_calc_n = -1
last_calc_color = None

c = [255] * 3


def init(cfg):
    global low, high, bar_length, diff, saturation, value
    bar_length = cfg['led']['bar-length']
    strength = cfg['viz']['colors']['modes']['strength']

    low = strength['low']
    high = strength['high']
    saturation = strength['saturation']
    value = strength['value']

    diff = high - low


def get_color(i, height):
    return c


def height_update(height):
    global c
    hue = diff * (height / bar_length) + low
    f = hsv_to_rgb(hue, saturation, value)
    f = [255 * i for i in f]
    c = f


def i_update(i, height):
    pass
