import importlib
import sys

from error import StrypeException, COLOR_STRATEGY_NOT_DEFINED

_cfg = {}

get_color = None
height_update = None
i_update = None


def init(cfg):
    global _cfg, get_color
    get_color = _get_color
    _cfg = cfg
    _col_cfg = cfg['viz']['colors']
    col_strat = get_color_strategy(_col_cfg['active-mode'])
    sys.modules[__name__].get_color = col_strat.get_color
    sys.modules[__name__].height_update = col_strat.height_update
    sys.modules[__name__].i_update = col_strat.i_update


def _get_color(i):
    raise StrypeException(COLOR_STRATEGY_NOT_DEFINED, 'Color strategy has not been defined yet. Check your config')


def get_color_strategy(strategy_name):
    col_strat = importlib.import_module('.' + strategy_name, 'colors')
    col_strat.init(_cfg)
    return col_strat
