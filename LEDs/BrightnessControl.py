from neopixel import *
import Colors

class LEDLevel:
	def __init__(index):
		myLevel = i
		firstLED = 64 - (8 * i)
		brightnessLevel = (31 * i)

BEGIN_LED = 0
END_LED = 63

# NeoPixel derived Variable
matrix = null

# Saved Pixel Color to Imitate
pixelColor = null

# Current LEDLevel Class
curLevel = null

# Current Brightness Index, [0,8]
curIndex = null

# Array [0,8] containing LEDLevel Classes
LEDLevelArray = []

savedMatrixRGB = []

def initializeArray:
	for i in range (0, 9):
		LEDLevelArray.append(LEDLevel(i))

# Going down a brightness level, set higher level row to BLACK
def downLevel:
	for i in range(curLevel.firstLED, LEDLevelArray[curIndex-1].firstLED):
		matrix.setPixelColor(i, Colors.BLACK)
		curLevel = LEDLevelArray[curIndex-1]
		curIndex = curLevel.myLevel
		matrix.setBrightness(curLevel.brightnessLevel)
		
# 
def upLevel:
	for i in range(LEDLevelArray[curIndex+1].firstLED, curLevel.firstLED):
		matrix.setPixelColor(i, pixelColor)
		curLevel = LEDLevelArray[curIndex+1]
		curIndex = curLevel.myLevel
		matrix.setBrightness(curLevel.brightnessLevel)

# Lamp enters brightness control mode, saves previous RGB Values beforehand
def enterControlMode():
	# Save RGB Values
	for i in range (0,63):
		savedMatrixRGB[i] = matrix.getPixelColor(i)
	# Set Brightness Levels
	for i in range (0, curLevel.firstLED):
		matrix.setPixelColor(i, Colors.BLACK)
	for i in range (curLevel.firstLED, 64):
		matrix.setPixelColor(i, pixelColor)

# Lamp exits brightness control mode, puts back RGB Values
def exitControlMode():
	# Returns Saved RGB Values
	for i in range (0,63):
		matrix.setPixelColor(i, savedMatrixRGB[i])

#Initialize, gets color from last LED
def __init__(matrix):
	self.matrix = matrix
	self.pixelColor = matrix.getPixelColor(END_LED)
	initializeArray()
	curLevel = LEDLevelArray[4]
	curIndex = 4