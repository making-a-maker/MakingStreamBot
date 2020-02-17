
import utils.led_colors as lc


def led_process(pixels, command):
    # Strip the ! from the command
    pixels.fill(lc.solid[command])
    pixels.show()

