from pprint import pprint

import pyaudio

p = pyaudio.PyAudio()
for i in range(p.get_device_count()):
    pprint(p.get_device_info_by_index(i))
