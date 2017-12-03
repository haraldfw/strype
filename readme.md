See complete configuration on the [wiki](https://github.com/haraldfw/strype/wiki).

# Configuration

To let strype read your audio output you have to set up a loopback interface in alsa. 

This is done by enabling the aloop-module in alsa and then telling mopidy to route audio to both your output and your loopback-interface.

## ALSA configuration
Enable loopback interface.
```
modprobe snd-aloop
```

## Mopidy configuration
Tell mopidy to send audio to output (`hw:0,0`) and loopback (`hw:1,0`)
```
[audio]
mixer = alsamixer
output = tee name=t ! queue ! audioresample ! alsasink device="hw:0,0" t. ! queue ! audioresample ! alsasink device="hw:1,0"
```
