import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np


class Plotter:

    func = None
    _rects = []
    _config = None

    def __init__(self, func, config):
        self.get_data = func
        self._config = config
        self._rects = np.zeros(self._config.bars)

    def animate(self):
        data = self.func()
        fig, ax = plt.subplots()

        i = 0



    def animate(i, ):
        for rect, yi in zip(rects, data[i]):
            rect.set_height(yi)
        line.set_data(x, data[i])
        return rects, line

    def start(self):
        anim = animation.FuncAnimation(
            fig, self.animate, frames=len(data), interval=40)

        frames = None
        wf = None
        ani = animation.FuncAnimation(
            fig, animate_single, frames,
            init_func=lambda: init(line), fargs=(line, stream, wf, max_y),
            interval=1000.0 / FPS, blit=True
        )
