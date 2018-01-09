import numpy
import spidev
import ws2812

_spi = None
_cols = []
_nled = -1


def init(nled, spi_dev):
    global _spi, _cols, _nled
    _nled = nled
    _spi = spidev.SpiDev()
    _spi.open(0, spi_dev)
    _cols = numpy.zeros((_nled, 3), dtype=numpy.uint8)


def clear():
    global _cols
    _cols = numpy.zeros((_nled, 3), dtype=numpy.uint8)


def show():
    ws2812.write2812(_spi, _cols)


def set_color(i, r, g, b):
    _cols[i] = numpy.array([g, r, b], dtype=numpy.uint8)
