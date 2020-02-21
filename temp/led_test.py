
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

while True:
    print("Red")
    pixels.fill((255, 0, 0, 0))
    pixels.show()
    time.sleep(5)

    print("Green")
    pixels.fill((0, 255, 0, 0))
    pixels.show()
    time.sleep(5)

    print("Blue")
    pixels.fill((0, 0, 255, 0))
    pixels.show()
    time.sleep(5)

    print("White")
    pixels.fill((0, 0, 0, 255))
    pixels.show()
    time.sleep(5)




