columns = []
decay = 0.9


def init(bars, decay_par):
    global columns, decay
    columns = [0] * bars
    decay = decay_par


def update_heights(data):
    for i, height in enumerate(data):
        height -= 8.0
        height /= 5
        if height < 0.05:
            height = 0
        elif height > 1.0:
            height = 1.0
        if height < columns[i]:
            columns[i] *= decay
        else:
            columns[i] = height
