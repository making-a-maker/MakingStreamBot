
import time

try:
    import board
    import neopixel
except ImportError as e:
    print("board or neopixel modules not installed - disabling LED string")
    leds_enabled = False


pixels = neopixel.NeoPixel(board.D18,
         144,
         brightness=0.25,
         auto_write=False, 
         bpp=4,
         pixel_order=(1, 0, 2, 3))

pixels.fill((255, 0, 0))






