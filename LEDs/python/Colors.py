from random import randint
import math
import numpy.random as rando

def getRGBArray(matrix):
	RGBArray = []

	for lednum in range (0,64):
		RGBArray = matrix.getPixelColor(lednum)

	return RGBArray

def setRGBArray(matrix, RGBArray):
	for lednum in range (0,64):
		matrix.setPixelColor(lednum, RGBArray[lednum])

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
	ColorArray = []
	numRGBs = 0
	red, green, blue = 0,0,0

	for lednum in range (0,64):
		if RGBArray[lednum] not 0:
			pixelRGB = ReverseColor(RGBArray[lednum])

			red += pow(pixelRGB[0], 2)
			green += pow(pixelRGB[1], 2)
			blue += pow(pixelRGB[2], 2)
			numRGBS++

	red = red / numRGBS
	green = green / numRGBS
	blue = blue / numRGBS

	# Values to be adjusted
	redVals = rando.normal(red, 25.5, numColors)
	greenVals = rando.normal(green, 25.5, numColors)
	blueVals = rando.normal(blue, 25.5, numColors)

	for i in range (0, numColors)
		ColorArray[i] = Color(redVals[i], greenVals[i], blueVals[i])

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
Output: None 
'''
def setRandomColor(matrix, binaryMatrix):
	for lednum in range (0,64):
		if binaryMatrix[lednum]:
			matrix.setPixelColor(lednum, randint(0, 0xFFFFFF))

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
Output: None 
'''
def setSingleColor(matrix, binaryMatrix, color):
	for lednum in range (0,64):
		if binaryMatrix[lednum] is None:
			continue
		elif binaryMatrix[lednum]:
			matrix.setPixelColor(lednum, color)
		else:
			matrix.setPixelColor(lednum, BLACK)

''' 
Convert the provided red, green, blue color to a 24-bit color value.
Each color component should be a value 0-255 where 0 is the lowest intensity
and 255 is the highest intensity.
'''
def Color(red, green, blue, white = 0):
	return (white << 24) | (red << 16)| (green << 8) | blue

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


