import matplotlib.pyplot as plt
import numpy as np
from matplotlib import animation


class Plotter:
    _data_get = None
    _heights = []
    _config = None
    _rects = None

    def __init__(self, func, config):
        """
         :type config: config.Config
        """
        self._data_get = func
        self._config = config
        self._heights = np.zeros(self._config.bars)
        self._rects = plt.bar(np.arange(self._config.bars), self._heights, align='center',
                              color='#b8ff5c', width=0.9)
        self._rs = [r for r in self._rects]

    def init(self):
        return self._rs

    def animate(self, i):
        data = self._data_get()

        for rect, yi in zip(self._rs, data):
            rect.set_height(yi)
        return self._rects

    def start(self):
        plt.tick_params(axis='x', colors='#072b57')
        plt.tick_params(axis='y', colors='#072b57')
        plt.xlabel('freq', color='#072b57')
        plt.ylabel('level', color='#072b57')
        plt.ylim(0, 1)

        dpi = plt.rcParams['figure.dpi']
        plt.rcParams['savefig.dpi'] = dpi
        plt.rcParams["figure.figsize"] = (1280.0 / dpi, 720.0 / dpi)

        fig = plt.figure()
        anim = animation.FuncAnimation(fig, self.animate, init_func=self.init, frames=200,
                                       interval=20,
                                       blit=True)

        plt.show()
