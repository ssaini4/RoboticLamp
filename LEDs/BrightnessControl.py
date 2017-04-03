from neopixel import *
import Colors

class LEDLevel:
	def __init__(index):
		myLevel = i
		firstLED = 64 - (8 * i)
		brightnessLevel = (31 * i)

BEGIN_LED = 0
END_LED = 63

matrix = null
pixelColor = null
curLevel = null
LEDLevelArray = []

def initializeArray:
	for i in range (0, 9):
		LEDLevelArray.append(LEDLevel(i))

# Sets RGB Value to Black of all LEDs up to (but not including) level first LED
def offLEDs(level):
	for i in range(curLevel.firstLED, LEDLevelArray[level].firstLED):
		matrix.setPixelColor(i, Colors.BLACK)
		
# 
def onLEDS(level):

# Lamp goes into control mode
def controlMode():

#Initialize, gets color from last LED
def __init__(matrix):
	self.matrix = matrix
	self.pixelColor = matrix.getPixelColor(END_LED)
	initializeArray()
	curLevel = LEDLevelArray[4]