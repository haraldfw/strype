import numpy

columns = []
spacers = []

_decay = 0.9


def init(bar_amount, decay):
    global columns, spacers, _decay
    spacers = [0] * 2
    columns = [0] * bar_amount
    _decay = decay


def update_heights(data):
    for i, height in enumerate(data):
        height -= 8.0
        height /= 5.5

        if height > 1.0:
            height = 1.0

        if height < columns[i]:
            columns[i] *= _decay
        else:
            columns[i] = height

        if columns[i] < 0.05:
            columns[i] = 0

    _update_spacers2(columns)


def _update_spacers2(heights):
    for i, v in enumerate(spacers):
        if v < 0.05:
            spacers[i] = 0
        else:
            spacers[i] = v * 0.7

    # if numpy.all(heights == 0.0):
    #     return

    _bar_amount = len(heights)
    fourths = _bar_amount // 4
    low = numpy.average(heights[:fourths]) > 0.8
    high = numpy.average(heights[_bar_amount - fourths:]) > 0.65

    if low:
        spacers[1] = 1
    if high:
        spacers[0] = 1
