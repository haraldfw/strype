import argparse
import signal
import sys

import pyaudio
import yaml
from logzero import logger

from ada_led_controller import LEDController
from audio import Audio
from audio_analysis import Analyzer
from prettyfier import Prettyfier


def read_config():
    with open('config.yml') as f:
        return yaml.load(f.read())


class Master:
    def __init__(self):
        cfg = read_config()
        audio_cfg = cfg['audio']
        led_cfg = cfg['led']
        viz_cfg = cfg['viz']
        self.audio = Audio(audio_cfg['channels'], audio_cfg['rate'], audio_cfg['chunk-size'], audio_cfg['device-index'])
        self.analyzer = Analyzer(led_cfg['bar-amount'], audio_cfg['rate'], audio_cfg['chunk-size'],
                                 audio_cfg['min-freq'],
                                 audio_cfg['max-freq'])
        self.pretty = Prettyfier(led_cfg['bar-amount'], viz_cfg['decay'])
        self.led_controller = LEDController(
            led_cfg['amount'], led_cfg['bar-amount'], led_cfg['bar-length'], led_cfg['spacer-length'])

    def run(self):
        while 1:
            heights = self.get_parsed_data()
            # print(heights)
            self.led_controller.update(heights)

    def get_parsed_data(self):
        data = self.analyzer.analyze(self.audio.read())
        self.pretty.update_heights(data)
        return self.pretty.get_heights()

    def close(self):
        self.audio.close()


master = None


def start_analyzer():
    global master
    logger.info('Starting Strype audio visualizer')
    master = Master()
    master.run()


def signal_handler():
    logger.info('User called exit. Exiting...')
    master.close()
    sys.exit(0)


def list_devices(args_given):
    detail = args_given.detail
    p = pyaudio.PyAudio()
    for i in range(p.get_device_count()):
        device = p.get_device_info_by_index(i)
        if not detail:
            device = {k: v for k, v in device.items() if
                      k in ['index', 'name', 'maxInputChannels', 'maxOutputChannels']}
        print(device)


def get_args():
    parser = argparse.ArgumentParser(description='Strype: Audio spectrum analyzer and visualizer.')
    parser.add_argument('-c', '--config', default='~/.config/strype/config.yml', dest='config_path',
                        help='Set the pull path for the config file.')
    parser.add_argument('-l', '--list-devices', dest='list_devices', action='store_true',
                        help='Lists available audio devices')
    parser.add_argument('-d', '--detail', dest='detail', action='store_true',
                        help='Makes list-devices output all details')
    return parser.parse_args()


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    args = get_args()
    if args.list_devices:
        list_devices(args)
    else:
        start_analyzer()
