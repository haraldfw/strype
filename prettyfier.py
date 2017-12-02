_columns = []
_decay = 0.9


def init(bar_amount, decay):
    global _columns, _decay
    _columns = [0] * bar_amount
    _decay = decay


def update_heights(data):
    for i, height in enumerate(data):
        height -= 8.0
        height /= 5.5

        if height > 1.0:
            height = 1.0

        if height < _columns[i]:
            _columns[i] *= _decay
        else:
            _columns[i] = height

        if _columns[i] < 0.05:
            _columns[i] = 0
