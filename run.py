from config import Config
import pyaudio


def main():
    config = Config()
    print(vars(config))
    p = pyaudio.PyAudio()
    dev_amount = p.get_device_count()
    for i in range(dev_amount):
        print(p.get_device_info_by_index(i))
    # device = p.get_device_info_by_index(config.audio_device)


if __name__ == '__main__':
    main()
