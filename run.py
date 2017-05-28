import pyaudio

from audio import Audio
from audio_analysis import Analyzer
from config import Config
from plotter import Plotter
from prettyfier import Prettyfier

analyzer = None
audio = None
pretty = None


def main():
    global audio, analyzer, pretty
    config = Config()
    config.start_scheduled_updates()

    p = pyaudio.PyAudio()
    for i in range(p.get_device_count()):
        print(p.get_device_info_by_index(i))

    audio = Audio(config)
    analyzer = Analyzer(config)
    pretty = Prettyfier(config)

    Plotter(get_parsed_data, config).start()

    # done
    audio.close()


def get_parsed_data():
    global audio, analyzer, pretty
    data = analyzer.analyze(audio.read())
    pretty.update_heights(data)
    return pretty.get_heights()


if __name__ == '__main__':
    main()
