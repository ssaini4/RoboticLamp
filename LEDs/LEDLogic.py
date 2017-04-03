import time

from neopixel import *
import brightnessControl

# 8 Brightness Levels
BRIGHTNESS_LEVEL0 = 0
BRIGHTNESS_LEVEL1 = 36
BRIGHTNESS_LEVEL2 = 72
BRIGHTNESS_LEVEL3 = 108
BRIGHTNESS_LEVEL4 = 144
BRIGHTNESS_LEVEL5 = 180
BRIGHTNESS_LEVEL6 = 216
BRIGHTNESS_LEVEL7 = 252

# LED strip configuration:
LED_COUNT      = 64      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = BRIGHTNESS_LEVEL4     # Start Brightness at Level 4
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)

if __name__ == '__main__':
	# Create NeoPixel object with appropriate configuration.
	matrix = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
	# Intialize the library (must be called once before other functions).
	matrix.begin()

	print ('Press Ctrl-C to quit.')
	while True:
		# Color wipe animations.
		colorWipe(strip, Color(255, 0, 0))  # Red wipe
		colorWipe(strip, Color(0, 255, 0))  # Blue wipe
		colorWipe(strip, Color(0, 0, 255))  # Green wipe
		# Theater chase animations.
		theaterChase(strip, Color(127, 127, 127))  # White theater chase
		theaterChase(strip, Color(127,   0,   0))  # Red theater chase
		theaterChase(strip, Color(  0,   0, 127))  # Blue theater chase
		# Rainbow animations.
		rainbow(strip)
		rainbowCycle(strip)
		theaterChaseRainbow(strip)
