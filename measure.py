bar_width = 8
length_per_led = 3.125

bars = 10
spacer_leds = 10
leds = 300


def measure():
    if bars % 2 == 0:
        total_spacers = (bars - 1) * spacer_leds
    else:
        total_spacers = bars * spacer_leds
    leds_per_bar = (leds - total_spacers) // bars

    height = (leds_per_bar * length_per_led) + length_per_led
    print(f'bars: {bars}')
    print(f'spacer leds: {spacer_leds}')
    print(f'Total spacer leds: {total_spacers}')
    print(f'leds used in bars: {leds_per_bar * bars}')
    print(f'leds per bar: {leds_per_bar}')
    print(f'total leds used: {total_spacers + leds_per_bar * bars}')
    print(f'height: {height}cm')
    print(f'width: {(bars - 1) * bar_width}cm')


def generate_config(total_leds, bar_amount, spacer_leds):
    total_spacers = (bars - 1) * spacer_leds
    leds_left_for_bars = total_leds - total_spacers
    leds_per_bar = leds_left_for_bars / bar_amount
    if leds_per_bar % 1:
        print(f'invalid config: leds left for bars does not divide by amount of bars')
    print(f'Leds per spacer: {spacer_leds}')
    print(f'leds for bars: {leds_left_for_bars}')
    print(f'total spacers: {total_spacers}')
    print(f'leds per bar:  {leds_per_bar}')
    print(f'Total width:  {(bars - 1)*bar_width}cm')



if __name__ == '__main__':
    generate_config(leds, bars, spacer_leds)
