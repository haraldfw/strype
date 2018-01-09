import argparse
import signal
import sys

import logging
import logzero
import pyaudio
import yaml
from logzero import logger

import led_controller
import audio
import audio_analysis as analyzer
import prettyfier as pretty
from error import StrypeException


def init():
    cfg = read_config()
    audio_cfg = cfg['audio']
    led_cfg = cfg['led']
    viz_cfg = cfg['viz']
    try:
        audio.init(audio_cfg['channels'], audio_cfg['rate'], audio_cfg['chunk-size'], audio_cfg['device-index'])
        analyzer.init(led_cfg['bar-amount'], audio_cfg['rate'], audio_cfg['chunk-size'],
                      audio_cfg['min-freq'],
                      audio_cfg['max-freq'])
        pretty.init(led_cfg['bar-amount'], viz_cfg['decay'])
        led_controller.init(led_cfg['amount'], led_cfg['bar-amount'], led_cfg['bar-length'], led_cfg['spacer-length'],
                            led_cfg, viz_cfg['colors'])
    except StrypeException as e:
        logger.error(e)
        sys.exit(1)


def read_config():
    with open('config.yml') as f:
        return yaml.load(f.read())


def run():
    while True:
        data = analyzer.analyze(audio.read())
        pretty.update_heights(data)
        led_controller.update(pretty.columns, pretty.spacers)


def close():
    audio.close()


def start_analyzer():
    logger.info('Starting Strype audio visualizer')
    init()
    logger.info('Initialization complete')
    run()


def signal_handler(a, b):
    logger.info('User called exit...')
    led_controller.clear()
    led_controller.show()
    logger.info('LEDs reset')
    close()
    logger.info('Audio stream closed')
    logger.info('Exited')
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
                        help='Sets logging level to debug. And makes \'list-devices\' output all details')
    return parser.parse_args()


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    args = get_args()
    if not args.detail:
        logzero.loglevel(logging.INFO)
    if args.list_devices:
        list_devices(args)
    else:
        start_analyzer()
