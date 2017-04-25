'''
TODO:
-Multithreads 
'''

from neopixel import *
import Colors
import Symbols
from random import randint

BEGIN_BOTTOM_BAR = 56
END_BOTTOM_BAR = 64

class ColorRotator:
	matrix = None

	curRed = 0
	curGreen = 0
	curBlue = 0
	random = False

	savedMatrixRGB = [None] * 64
	rotator_binMatrix = [None] * 64

	# nextColor does not handle timing.
	def nextColor(self):
		self.curBlue = self.curBlue + 127

		if self.curBlue > 255:
			self.curBlue = 0
			self.curGreen = self.curGreen + 127
			if self.curGreen > 255:
				self.curGreen = 0
				self.curRed = self.curRed + 127
				if self.curRed > 255:
					self.curRed = 0

		if self.curBlue == 0 and self.curGreen == 0 and self.curRed == 0:
			# set Random
			self.random = True
			Colors.setRandomColor(self.matrix, self.rotator_binMatrix)
		else:
			self.random = False
			Colors.setSingleColor(self.matrix, self.rotator_binMatrix, Colors.Color(self.curRed, self.curGreen, self.curBlue))

		print str(self.curRed) + "," + str(self.curGreen) + "," + str(self.curBlue)

	def enterColorRotator(self):
		self.savedMatrixRGB = Colors.getRGBArray(self.matrix)		

		# Get current avg RGB Values
		curAvgRGB = Colors.getAvgColor(Colors.getRGBArray(self.matrix), 1)

		self.curRed,self.curGreen,self.curBlue = Colors.ReverseColor(curAvgRGB)

		Colors.setSingleColor(self.matrix, self.rotator_binMatrix, Colors.Color(self.curRed,self.curGreen,self.curBlue))
		random = False

	def exitColorRotator(self):

		for lednum in range (0, 64):
			if self.savedMatrixRGB[lednum] != 0x00: # If not black LED
				if self.random == True:
					self.savedMAtrixRGB[lednum] = randint(0, 0xFFFFFF)
				else:
					self.savedMatrixRGB[lednum] = Colors.Color(self.curRed, self.curGreen, self.curBlue)

		Colors.setRGBArray(self.matrix, self.savedMatrixRGB)

	def __init__(self, matrix):
		self.matrix = matrix
		self.rotator_binMatrix = Symbols.processSymbol(Symbols.COLOR_ROTATOR_SCREEN)
