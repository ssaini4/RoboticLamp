'''
TODO:
-Multithreads 
'''

from neopixel import *
import Colors

class RecognitionMode:
	matrix = None

	windowIdx = None
	windowRGBArray = [None] * 5

	savedMatrixRGB = [None] * 64

	CompletionBarBinary = [None] * 5
	CompletionBarIdx = None

	SymbolColor = None # For now Symbol will be one color

	# Displays symbol with a level (0-4) that shows a bar at the bottom TODO
	def displaySymbol(symbolMatrix, level):
		# Put Symbol on LED Matrix
		Colors.setSingleColor(self.matrix, symbolMatrix, SymbolColor)
		# Overlay with Completion Bar
		Colors.setSingleColor(self.matrix, CompletionBarBinary[level], Colors.GREEN)
		self.CompletionBarIdx = 0

	# Decreases bottom bar, doesn't touch other LEDs TODO
	# Sets it red to indicate loss of lock
	# Returns TRUE if already 0
	def downLevel(self):
		if self.CompletionBarIdx != 0:
			self.CompletionBarIdx -= 1
			Colors.setSingleColor(self.matrix, CompletionBarBinary[self.CompletionBarIdx], Colors.RED)

			return False
		else:
			return True

	# Increases bottom bar, doesn't touch other LEDs TODO
	# Sets it green to indicate close lock
	# Returns TRUE if at 4 (100%)
	def upLevel(self):
		if self.windowIdx != 4:
			self.windowIdx += 1
			Colors.setSingleColor(self.matrix, CompletionBarBinary[self.CompletionBarIdx], Colors.GREEN)
			
			if self.windowIdx != 4:
				return False
			else:
				return True
		else:
			return True

	# No lock on a gesture - continue cycling windows
	# Resets completion bar
	def noLock(self):
		self.windowIdx = (self.windowIdx + 1) % 5
		Colors.setRGBArray(self.matrix, windowRGBArray[self.windowIdx])
		self.CompletionBarIdx = 0

	def enterRecognitionMode(self, average = False, random = False):
		# Save previous RGB Array
		for i in range (0, 64):
			self.savedMatrixRGB[i] = self.matrix.getPixelColor(i)
		# 5 Windows
		if average:
			prevRGBArray = Colors.getRGBArray(self.matrix)

			AverageColors = Colors.getAvgColor(prevRGBArray, 5)
			for winNum in range (0,5):
				windowRGBArray[winNum] = Colors.getSingleColor(Symbols.processSymbol(Symbols.RECOGNITION_IN_PERCENT[winNum]), AverageColors[winNum])

			# Symbol color gets one of the Windows
			SymbolColor = randint(0,4)

		elif random:
			for winNum in range (0,5):
				windowRGBArray[winNum] = Colors.getRandomColor(Symbols.processSymbol(Symbols.RECOGNITION_IN_PERCENT[winNum]))

			# Symbol gets one random color for all LEDs
			SymbolColor = randint(0, 0xFFFFFF)

		else:
			pass
			#ERROR

		# Needs bottom bar level array TODO
		for i in range (0,5):
			CompletionBarBinary = Symbols.PERCENT_BAR[i]

		self.windowIdx = 0
		self.CompletionBaryIdx = 0
		Colors.setRGBArray(self.matrix, windowRGBArray[self.windowIdx])

	def exitRecognitionMode(self):
		Colors.setRGBArray(self.matrix, self.savedMatrixRGB)

	def __init__(self, matrix):
		self.matrix = matrix
		self.windowIdx = -1
