import struct

import math
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import pyaudio

from config import Config

TITLE = ''
WIDTH = 1280
HEIGHT = 720
FPS = 25.0

nFFT = 256
BUF_SIZE = 4 * nFFT
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100


def fft(data=None, trim_by=10, log_scale=False, div_by=100):
    left, right = np.split(np.abs(np.fft.fft(data)), 2)
    ys = np.add(left, right[::-1])
    if log_scale:
        ys = np.multiply(20, np.log10(ys))
    xs = np.arange(BUF_SIZE / 2, dtype=float)
    if trim_by:
        i = int((BUF_SIZE / 2) / trim_by)
        ys = ys[:i]
        xs = xs[:i] * RATE / BUF_SIZE
    if div_by:
        ys = ys / float(div_by)
    return xs, ys


def animate_single(i, line, stream, wf, max_y):
    n = int(max(stream.get_read_available() / nFFT, 1) * nFFT)
    data = stream.read(n)

    y = np.array(struct.unpack("%dh" % (n * CHANNELS), data)) / max_y
    y = y.flatten()

    left, right = np.split(np.abs(np.fft.fft(y)), 2)
    ys = np.add(left, right[::-1])
    ys = np.multiply(20, np.log10(ys))
    ys = np.clip(ys, a_min=0, a_max=100000000)
    xs = np.arange(BUF_SIZE, dtype=float)

    j = BUF_SIZE
    ys = ys[:j]
    xs = xs[:j] * RATE / BUF_SIZE
    # ys = np.divide(100, ys)
    ys = ys / 100.0

    line.set_xdata(xs)
    line.set_ydata(ys)
    return line,


def animate(i, line, stream, wf, max_y):
    # Read n*nFFT frames from stream, n > 0
    n = int(max(stream.get_read_available() / nFFT, 1) * nFFT)
    data = stream.read(n)

    y = np.array(struct.unpack("%dh" % (n * CHANNELS), data)) / max_y

    y_l = np.fft.fft(y[::2], nFFT)
    y_r = np.fft.fft(y[1::2], nFFT)

    # Sewing FFT of two channels together, DC part uses right channel's
    y = np.abs(np.hstack((y_l[-nFFT // 2:-1], y_r[:nFFT // 2])).flatten())

    line.set_ydata([20 * np.log10(x + 1) for x in y])
    return line,


def init(line):
    # This data is a clear frame for animation
    line.set_ydata(np.zeros(nFFT - 1))
    return line,


def main():
    dpi = plt.rcParams['figure.dpi']
    plt.rcParams['savefig.dpi'] = dpi
    plt.rcParams["figure.figsize"] = (1.0 * WIDTH / dpi, 1.0 * HEIGHT / dpi)

    fig = plt.figure()

    # Frequency range
    x_f = 1.0 * np.arange(-nFFT / 2 + 1, nFFT / 2) / nFFT * RATE
    ax = fig.add_subplot(111, title=TITLE, xlim=(0, RATE / 2),
                         ylim=(0, 2 * np.pi * nFFT ** 2 / RATE))
    ax.set_yscale('symlog', linthreshy=(nFFT ** 0.5) / 100)

    line, = ax.plot(x_f, np.zeros(nFFT - 1))

    # Change x tick labels for left channel
    def change_xlabel(evt):
        labels = [label.get_text().replace(u'\u2212', '')
                  for label in ax.get_xticklabels()]
        ax.set_xticklabels(labels)
        fig.canvas.mpl_disconnect(draw_id)

    draw_id = fig.canvas.mpl_connect('draw_event', change_xlabel)

    p_aud = pyaudio.PyAudio()
    # Used for normalizing signal. If use paFloat32, then it's already -1..1.
    # Because of saving wave, paInt16 will be easier.
    max_y = 2.0 ** (p_aud.get_sample_size(FORMAT) * 8 - 1)

    frames = None
    wf = None

    stream = p_aud.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=BUF_SIZE,
                        input_device_index=Config().audio_device)

    ani = animation.FuncAnimation(
        fig, animate_single, frames,
        init_func=lambda: init(line), fargs=(line, stream, wf, max_y),
        interval=1000.0 / FPS, blit=True
    )

    plt.show()

    stream.stop_stream()
    stream.close()
    p_aud.terminate()


if __name__ == '__main__':
    main()
