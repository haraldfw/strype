bar_width = 8
length_per_led = 3.125
bars = 10
spacer_leds = 4
leds = 160


def measure():
    leds_per_bar = (leds - (bars * spacer_leds)) / bars

    height = (leds_per_bar * length_per_led) + length_per_led
    print(f'bars: {bars}')
    print(f'spacer leds: {spacer_leds}')
    print(f'leds per bar: {leds_per_bar}')
    print(f'height: {height}cm')
    print(f'width: {(bars - 1) * bar_width}cm')


if __name__ == '__main__':
    measure()
