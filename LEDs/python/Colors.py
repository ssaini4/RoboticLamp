''' Sets all LEDs to be lit a random color. All other Black.
Input:
	matrix - Neopixel Wrapper
	binaryMatrix - Length 64 Binary Array
Output: None '''
def setRandomColor(matrix, binaryMatrix):
	for lednum in range (0,63):
                pass

""" Sets all LEDs to be lit a single color. All other Black.
Input:
        matrix - Neopixel Wrapper
        binaryMatrix - Length 64 binary Array
        color - 24 Bit RGB Value
Output: None """
def setSingleColor(matrix, binaryMatrix, color):
	for lednum in range (0,63):
		if binaryMatrix[lednum]:
			matrix.setPixelColor(lednum, color)
		else:
			matrix.setPixelColor(lednum, BLACK)

def Color(red, green, blue, white = 0):
	"""Convert the provided red, green, blue color to a 24-bit color value.
	Each color component should be a value 0-255 where 0 is the lowest intensity
	and 255 is the highest intensity.
	"""
	return (white << 24) | (red << 16)| (green << 8) | blue

"""
Reverse action of Color.
Input: 24 Bit RGB Value
Output: Length 3 Byte Array [Red, Green, Blue]
"""
def ReverseColor(color):
	return [
		((color >> 16) & 0xFF),
		((color >> 8) & 0xFF),
		(color & 0xFF)
	]

BLACK = Color(0, 0, 0)
