from neopixel import *
import Colors
import Symbols
import datetime
import time

# Time that LEDs go off to simulate blinking
BLINK_DURATION = 0.5

class LEDClock:
	matrix = None

	savedMatrixRGB = [None] * 64

	"""
	Shows time on the LEDs for a certain duration. (Default 2 seconds) 
	Flashes hours then minutes, 1 second each, or total time/2 for each.
	input:
		int duration - duration to show time (in seconds)
	output: none
	"""
	def showTime(self, duration = 2):
		showTime = min(1, (duration - (2*BLINK_DURATION)) / 2)

		timeElapsed = 0
		chooseShow = True #True = Hour, False = Minute
		curTime = None

		while(timeElapsed < duration):
			# Generate new time if null or changed
			if curTime == None or curTime != datetime.datetime.now():
				curTime = datetime.datetime.now()
				
				timeArray = str(datetime.datetime.now()).split(" ")
				timeArray = timeArray[1].split(":")

				intArray = [None] * 4

				for i in range (0,2):
					for j in range (0,2):
						intArray[ (2*i) + j] = int(timeArray[i][j])

				timeMatrix = [[None] * 64] * 4
				for i in range (0,4):
					timeMatrix[i] = Symbols.timeBinaryProcessor(intArray[i], i)

				hourMatrix = Symbols.binaryMatrixAdder([timeMatrix[0], timeMatrix[1]])
				minuteMatrix = Symbols.binaryMatrixAdder([timeMatrix[2], timeMatrix[3]])

			if chooseShow: #show Hour
				hourRGB = Colors.getSingleColor(hourMatrix, Colors.GREEN)
				colonRGB = Colors.getSingleColor(Symbols.processSymbol(Symbols.TIME_COLON), Colors.SKYBLUE)
                                # ADD CYAN-COLORED COLONS by creating an "RGBArrayAdder" method
				hourcolonRGB = Colors.RGBArrayAdder([hourRGB, colonRGB])

				Colors.setRGBArray(self.matrix, hourcolonRGB)
				chooseShow = False
			else: #show Minute
				Colors.setSingleColor(self.matrix, minuteMatrix, Colors.RED)
				chooseShow = True

			time.sleep(showTime)

			Colors.setOFF(self.matrix)

			time.sleep(BLINK_DURATION)

			timeElapsed = timeElapsed + showTime + BLINK_DURATION

	def enterLEDClock(self):
		# Save previous RGB Array
		for i in range (0, 64):
			self.savedMatrixRGB[i] = self.matrix.getPixelColor(i)

	def exitLEDClock(self):
		# Returns previous array
		Colors.setRGBArray(self.matrix, self.savedMatrixRGB)

	def __init__(self, matrix):
		self.matrix = matrix
