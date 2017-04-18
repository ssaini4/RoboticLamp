from neopixel import *
import Colors
import Symbols

class RecognitionEntrance:
	
	matrix = None

	windowIdx = None
	windowRGBArray = [None] * 5

	savedMatrixRGB = [None] * 64

	# Returns True if already 0%, False otherwise
	def downLevel(self):
		if self.windowIdx != 0:
			self.windowIdx -= 1
			Colors.setRGBArray(self.matrix, self.windowRGBArray[self.windowIdx])

			return False
		else:
			return True

	# Returns True if 100%, False otherwise
	def upLevel(self):
		if self.windowIdx != 4:
			self.windowIdx += 1
			Colors.setRGBArray(self.matrix, self.windowRGBArray[self.windowIdx])
			
			if self.windowIdx != 4:
				return False
			else:
				return True
		else:
			return True
		
        # Defaults to Average!
	def enterRecognitionEntrance(self, average = False, random = False):
		# Save previous RGB Array
		for i in range (0, 64):
			self.savedMatrixRGB[i] = self.matrix.getPixelColor(i)
		# 5 Windows
		if average:
			prevRGBArray = Colors.getRGBArray(self.matrix)

			AverageColors = Colors.getAvgColor(prevRGBArray, 5)
			for winNum in range (0,5):
				self.windowRGBArray[winNum] = Colors.getSingleColor(Symbols.processSymbol(Symbols.RECOGNITION_IN_PERCENT[winNum]), AverageColors[winNum])

		elif random:
			for winNum in range (0,5):
				self.windowRGBArray[winNum] = Colors.getRandomColor(Symbols.processSymbol(Symbols.RECOGNITION_IN_PERCENT[winNum]))

		else:
			pass
			#ERROR

		self.windowIdx = 0
		Colors.setRGBArray(self.matrix, self.windowRGBArray[self.windowIdx])

	def exitRecognitionEntrance(self):
        Colors.setRGBArray(self.matrix, self.savedMatrixRGB)

	def __init__(self, matrix):
		self.matrix = matrix
		self.windowIdx = -1
