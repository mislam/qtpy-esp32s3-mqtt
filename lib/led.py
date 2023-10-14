import board
import neopixel
import time

# Neopixel colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (255, 0, 255)

ON = True
OFF = False


class _LED:
    def __init__(self) -> None:
        # Initialize the Neopixel LED
        self._neo = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.3)

    def blink(self, color, *, freq: float = 0.3):
        self._neo.fill(color)
        time.sleep(freq)
        self._neo.fill((0, 0, 0))
        time.sleep(freq)

    def on(self, color, *, wait: float = None):
        self._neo.fill(color)
        if wait is not None:
            time.sleep(wait)

    def off(self):
        self._neo.fill((0, 0, 0))


led = _LED()
