import audio_analysis
from audio import Audio
from audio_analysis import Analyzer
from config import Config
import pyaudio

from plotter import Plotter


analyzer = None
audio = None


def main():
    global audio, analyzer
    config = Config()
    print(vars(config))
    p = pyaudio.PyAudio()
    dev_amount = p.get_device_count()
    for i in range(dev_amount):
        print(p.get_device_info_by_index(i))

    audio = Audio(config)
    analyzer = Analyzer(config)
    plotter = Plotter(get_parsed_data, config)

    audio.close()


def get_parsed_data():
    global audio, analyzer
    return analyzer.parse(audio.max_y, *audio.read())

if __name__ == '__main__':
    main()
