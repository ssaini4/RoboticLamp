from neopixel import *
import Colors

matrix = None

windowIdx = None
windowRGBArray = [None] * 5

# Returns True if already 0%, False otherwise
def downLevel(self):
	if self.windowIdx not 0:
		self.windowIdx--
		Colors.setRGBArray(self.matrix, windowRGBArray[self.windowIdx])

		return False
	else:
		return True

# Returns True if 100%, False otherwise
def upLevel(self):
	if self.windowIdx not 4:
		self.windowIdx++
		Colors.setRGBArray(self.matrix, windowRGBArray[self.windowIdx])
		
		if self.windowIdx not 4:
			return False
		else:
			return True
	else:
		return True

def enterRecognitionEntrance(self, average, random):
	# 5 Windows
	if average:
		prevRGBArray = Colors.getRGBArray(self.matrix)

		AverageColors = Colors.getAvgColor(prevRGBArray, 5)
		for winNum in range (0,5):
			windowRGBArray[winNum] = Colors.getSingleColor(Symbols.processSymbol(Symbols.RECOGNITION_IN_PERCENT[winNum]), AverageColors[winNum])

	else if random:
		for winNum in range (0,5):
			windowRGBArray[winNum] = Colors.getRandomColor(Symbols.processSymbol(Symbols.RECOGNITION_IN_PERCENT[winNum]))

	else:
		pass
		#ERROR

	self.windowIdx = 0
	Colors.setRGBArray(self.matrix, windowRGBArray[self.windowIdx])

def exitRecognitionEntrance(self):

def __init__(self, matrix):
	self.matrix = matrix
	self.windowIdx = -1