'''
TODO:
-Multithreads 
'''

from neopixel import *
import Colors
import Symbols
from random import randint

class RecognitionMode:
	matrix = None

	windowIdx = None
	windowRGBArray = [None] * 5

	savedMatrixRGB = [None] * 64

	CompletionBarBinary = [None] * 5
	CompletionBarIdx = None

	SymbolColor = None # For now Symbol will be one color

	# Displays symbol with a level (0-4) that shows a bar at the bottom TODO
	def displaySymbol(self, symbolMatrix, level):
		# Put Symbol on LED Matrix
		print self.SymbolColor
		Colors.setSingleColor(self.matrix, symbolMatrix, self.SymbolColor)
		# Overlay with Completion Bar
		#Colors.setSingleColor(self.matrix, self.CompletionBarBinary[level], Colors.GREEN)
		self.CompletionBarIdx = 0

	# Decreases bottom bar, doesn't touch other LEDs TODO
	# Sets it red to indicate loss of lock
	# Returns TRUE if already 0
	def downLevel(self):
                print "needs rework!"
                return False
                
		if self.CompletionBarIdx != 0:
			self.CompletionBarIdx -= 1
			Colors.setSingleColor(self.matrix, self.CompletionBarBinary[self.CompletionBarIdx], Colors.RED)

			return False
		else:
			return True

	# Increases bottom bar, doesn't touch other LEDs TODO
	# Sets it green to indicate close lock
	# Returns TRUE if at 4 (100%)
	def upLevel(self):
                print "needs rework!"
                return False
		if self.CompletionBarIdx != 4:
			self.CompletionBarIdx += 1
			
			Colors.setSingleColor(self.matrix, self.CompletionBarBinary[self.CompletionBarIdx], Colors.GREEN)

			if self.CompletionBarIdx != 4:
				return False
			else:
				return True
		else:
			return True

	# No lock on a gesture - continue cycling windows
	# Resets completion bar
	def noLock(self):
		self.windowIdx = (self.windowIdx + 1) % 5
		Colors.setRGBArray(self.matrix, self.windowRGBArray[self.windowIdx])
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
				self.windowRGBArray[winNum] = Colors.getSingleColor(Symbols.processSymbol(Symbols.RECOGNITION_IN_PERCENT[winNum]), AverageColors[winNum])

			# Symbol color gets one of the Windows
			self.SymbolColor = AverageColors[randint(0,4)]

		elif random:
			for winNum in range (0,5):
				self.windowRGBArray[winNum] = Colors.getRandomColor(Symbols.processSymbol(Symbols.RECOGNITION_IN_PERCENT[winNum]))

			# Symbol gets one random color for all LEDs
			self.SymbolColor = randint(0x00, 0xFFFFFF)

		else:
			pass
			#ERROR

		for i in range (0,5):
			self.CompletionBarBinary[i] = Symbols.PERCENT_BAR[i]

		self.windowIdx = 0
		self.CompletionBarIdx = 0
		Colors.setRGBArray(self.matrix, self.windowRGBArray[self.windowIdx])

	def exitRecognitionMode(self):
		Colors.setRGBArray(self.matrix, self.savedMatrixRGB)

	def __init__(self, matrix):
		self.matrix = matrix
		self.windowIdx = -1
