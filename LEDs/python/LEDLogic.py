import time

from neopixel import *
import brightnessControl

# LED strip configuration:
LED_COUNT      = 64      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 4 * 31  # Start Brightness at Level 4
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
PIXEL_COLOR    = null

if __name__ == '__main__':
	# Create NeoPixel object with appropriate configuration.
	matrix = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
	# Intialize the library (must be called once before other functions).
	matrix.begin()

	print ('Press Ctrl-C to quit.')


