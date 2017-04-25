from random import randint
import math
import numpy.random as rando

def getRGBArray(matrix):
	RGBArray = [None] * 64

	for lednum in range (0,64):
		RGBArray[lednum] = matrix.getPixelColor(lednum)

	return RGBArray

def setRGBArray(matrix, RGBArray):
	for lednum in range (0,64):
		if RGBArray[lednum] != None:
			matrix.setPixelColor(lednum, RGBArray[lednum])

	matrix.show()

'''
Combines 64-bit RGB Arrays by adding the values together
Input: RGBArrays - Array of 64-bit RGB Arrays
Output finalRGBArray - Single added 64-bit RGB Array
'''
def RGBArrayAdder(RGBArrays):
	finalRGBArray = [0x000000] * 64

	for lednum in range (0,64):

		red = 0
		green = 0
		blue = 0

		for matrixNum in range (0, len(RGBArrays)):
			addR,addG,addB = ReverseColor(RGBArrays[matrixNum][lednum])

			red = red + addR
			green = green + addG
			blue = blue + addB

		finalRGBArray[lednum] = Color(red,green,blue)

	return finalRGBArray

''' 
Grabs a number of colors using current matrix RGB Values
using a Gaussian Normal Distribution on each RGB Value
with Standard Deviation 255 / 10.
Input:
	RGBArray - Length 64 RGB Array
	numColors - Number of colors to output
Output:
	ColorArray[numColors]
'''
def getAvgColor(RGBArray, numColors):
	ColorArray = [None] * numColors
	numRGBs = 0
	red, green, blue = 0,0,0

	for lednum in range (0,64):
		if RGBArray[lednum] != 0:
			pixelRGB = ReverseColor(RGBArray[lednum])                   
			
			red += pow(pixelRGB[0], 2)
			green += pow(pixelRGB[1], 2)
			blue += pow(pixelRGB[2], 2)
			numRGBs += 1

	# NEed to add Divide by 0 Check

	red = math.sqrt(red / numRGBs)
	green = math.sqrt(green / numRGBs)
	blue = math.sqrt(blue / numRGBs)

	#print str(hex(red)) + " " + str(hex(green)) + " " + str(hex(blue))

	if numColors == 1:
		return Color(int(red), int(green), int(blue))

	# Values to be adjusted
	redVals = rando.normal(red, 15.5, numColors)
	greenVals = rando.normal(green, 15.5, numColors)
	blueVals = rando.normal(blue, 15.5, numColors)

	for i in range (0, numColors):
		ColorArray[i] = Color(int(redVals[i]), int(greenVals[i]), int(blueVals[i]))

	return ColorArray

''' 
Gets random color for each LED. All other Black.
Input:
	binaryMatrix - Length 64 Binary Array
Output: RGBArray[64] 
'''
def getRandomColor(binaryMatrix):
	RGBArray = [None] * 64

	for lednum in range (0,64):
		if binaryMatrix[lednum]:
			RGBArray[lednum] = randint(0, 0xFFFFFF)
		else:
			RGBArray[lednum] = 0

	return RGBArray

''' 
Sets all LEDs to be lit a random color. All other Black.
Input:
	matrix - Neopixel Wrapper
	binaryMatrix - Length 64 Binary Array
    startLED - First LED to set (default 0)
    endLED - Last LED to set (default 64)
Output: None 
'''
def setRandomColor(matrix, binaryMatrix, startLED = 0, endLED = 64):
	for lednum in range (startLED, endLED):
		if binaryMatrix[lednum]:
			matrix.setPixelColor(lednum, randint(0, 0xFFFFFF))

	matrix.show()

''' 
Gets RGB Array for Single Color. All other Black.
Input:
        binaryMatrix - Length 64 binary Array
        color - 24 Bit RGB Value
Output: RGBArray[64]
'''
def getSingleColor(binaryMatrix, color):
	RGBArray = [None] * 64

	for lednum in range (0,64):
		if binaryMatrix[lednum]:
			RGBArray[lednum] = color
		else:
			RGBArray[lednum] = 0

	return RGBArray

''' 
Sets all LEDs to be lit a single color. All other Black.
Input:
    matrix - Neopixel Wrapper
    binaryMatrix - Length 64 binary Array
    color - 24 Bit RGB Value
    startLED - First LED to set (default 0)
    endLED - Last LED to set (default 64)
Output: None 
'''
def setSingleColor(matrix, binaryMatrix, color, startLED = 0, endLED = 64):
    # Need to check if the matrix.setPixelColor
    # saves from previous iterations

	for lednum in range (startLED, endLED):
                try:
                        if binaryMatrix[lednum]:
                                matrix.setPixelColor(lednum, color)
                        else:
                                matrix.setPixelColor(lednum, BLACK)
                except IndexError:
                        print "skipped "+ str(lednum)
                        
	matrix.show()
	
'''
Turns off all LEDs
'''	
def setOFF(matrix, startLED = 0, endLED = 64):
	for lednum in range (startLED, endLED):
		matrix.setPixelColor(lednum, BLACK)

	matrix.show()

''' 
Convert the provided red, green, blue color to a 24-bit color value.
Each color component should be a value 0-255 where 0 is the lowest intensity
and 255 is the highest intensity.
'''
def Color(red, green, blue, white = 0):
	return (white << 24) | (clip(red) << 16)| (clip(green) << 8) | clip(blue)

'''
Reverse action of Color.
Input: 24 Bit RGB Value
Output: Length 3 Byte Array [Red, Green, Blue]
'''
def ReverseColor(color):
	return [
		((color >> 16) & 0xFF),
		((color >> 8) & 0xFF),
		(color & 0xFF)
	]

# Clips RGB Values to be 0 to 255
def clip(color):
        if color > 255:
                return 255
        elif color < 0:
                return 0
        else:
                return color

'''
COLORS
From: https://en.wikipedia.org/wiki/Web_colors
'''


# Pink Colors
PINK 	= 0xFFC0CB
HOTPINK = 0xFF69B4

# Red Colors
SALMON 	= 0xFA8072
RED 	= 0xFF0000

# Orange Colors
CORAL  = 0xFF7F50
ORANGE = 0xFFA500

# Yellow Colors
YELLOW 	= 0xFFFF00
GOLD	= 0xFFD700

# Brown Colors
TAN		= 0xD2B48C
MAROON 	= 0x800000

# Green Colors
OLIVE 	= 0x808000
LIME 	= 0x00FF00
GREEN 	= 0x008000

# Cyan Colors
AQUA 	= 0x00FFFF
TEAL 	= 0x008080

# Blue Colors
SKYBLUE = 0x87CEEB
BLUE 	= 0x0000FF

# Purple Colors
FUCHSIA = 0xFF00FF
PURPLE 	= 0x800080

# White Colors
WHITE 	= 0xFFFFFF
BEIGE	= 0xF5F5DC

# Black Colors
BLACK 	= 0x000000
SILVER 	= 0xC0C0C0
GRAY 	= 0x808080


