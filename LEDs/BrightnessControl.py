from neopixel import *
import Colors

LEVEL0 = 0
LEVEL1 = 31
LEVEL2 = 62
LEVEL3 = 93
LEVEL4 = 124
LEVEL5 = 155
LEVEL6 = 186
LEVEL7 = 217
LEVEL8 = 248

LEVEL0_FIRSTLED = 64
LEVEL1_FIRSTLED = 56
LEVEL2_FIRSTLED = 48
LEVEL3_FIRSTLED = 40
LEVEL4_FIRSTLED = 32 
LEVEL5_FIRSTLED = 24
LEVEL6_FIRSTLED = 16
LEVEL7_FIRSTLED = 8
LEVEL8_FIRSTLED = 0

matrix = null
brightnessLevel = BRIGHTNESS_LEVEL4

def initialize(matrix, brightnessLevel):
	self.matrix = matrix
	if brightnessLevel not null:
		self.brightnessLevel = brightnessLevel

# Sets RGB Value to Black of all LEDs up to (but not including) index
def offLEDs(index):
	for i in range(0,index - 1):
		matrix.setPixelColor(i, Colors.BLACK)

# Lamp goes into control mode
def controlMode():

