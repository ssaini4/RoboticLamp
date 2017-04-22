from neopixel import *
import time

# LED strip configuration:
LED_COUNT      = 64      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255	 # Highest Brightness
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
PIXEL_COLOR    = None

matrix = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)

matrix.begin()

for lednum in range (0,64):
	# Set R(255) G(255) B(255)
	matrix.setPixelColor(lednum, 0xFFFFFF)

print "lighting bright white for 30 minutes, please wait..."

matrix.show()

time.sleep(1800)

choice = "Are LEDs still bright white? y or n - "

while True:
	if choice == "y":
		print "test PASSED!"
	elif choice == "n":
		print "test FAILED!"
	else:
		print "Try again."

for lednum in range (0,64):
	# Set back to black
	matrix.setPixelColor(lednum, 0x000000)

print "done."