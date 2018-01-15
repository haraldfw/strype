col_static_r = -1
col_static_g = -1
col_static_b = -1


def init(cfg):
    global col_static_r, col_static_g, col_static_b
    col_cfg = cfg['viz']['colors']
    col_static_r = col_cfg['modes']['static']['r']
    col_static_g = col_cfg['modes']['static']['g']
    col_static_b = col_cfg['modes']['static']['b']


def height_update(height):
    pass


def i_update(i, height):
    pass


def get_color(i, height):
    return col_static_r, col_static_g, col_static_b
