import time

from neopixel import *
import Colors

# LED strip configuration:
LED_COUNT      = 64      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 4 * 31  # Start Brightness at Level 4
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
PIXEL_COLOR    = None

matrix = None

class LEDLevel:
        myLevel = None
        firstLED = None
        brightnessLevel = None
        
	def __init__(self, index):
		self.myLevel = index
		self.firstLED = 64 - (8 * index)
		self.brightnessLevel = int((index * index) * 3.99)
		print self.brightnessLevel
		
class BrightnessCtrl:

        BEGIN_LED = 0
        END_LED = 63

        # Saved Pixel Color to Imitate
        pixelColor = None

        # Current LEDLevel Class
        curLevel = None

        # Current Brightness Index, [0,8]
        curIndex = None

        # Array [0,8] containing LEDLevel Classes
        LEDLevelArray = [None] * 9

        savedMatrixRGB = [None] * 64

        def initializeArray(self):
                for i in range (0, 9):
                        self.LEDLevelArray[i] = LEDLevel(index = i)

        # Going down a brightness level, set higher level row to BLACK
        def downLevel(self):
                print "downlevel"

                if self.curIndex == 0:
                        print "brightness too low. exiting"
                        return
                
                global matrix
                for i in range(self.curLevel.firstLED, self.LEDLevelArray[self.curIndex-1].firstLED):
                        matrix.setPixelColor(i, Colors.BLACK)

                self.curLevel = self.LEDLevelArray[self.curIndex-1]
                self.curIndex = self.curLevel.myLevel
                matrix.setBrightness(self.curLevel.brightnessLevel)
                matrix.show()

                        
        # 
        def upLevel(self):
                print "uplevel"

                if self.curIndex == 8:
                        print "brightness too high. exiting"
                        return

                global matrix

                print self.curLevel.firstLED
                print self.curIndex
                
                for i in range(self.LEDLevelArray[self.curIndex+1].firstLED, self.curLevel.firstLED):
                        matrix.setPixelColor(i, self.pixelColor)
                self.curLevel = self.LEDLevelArray[self.curIndex+1]
                self.curIndex = self.curLevel.myLevel
                matrix.setBrightness(self.curLevel.brightnessLevel)
                matrix.show()
                
        # Lamp enters brightness control mode, saves previous RGB Values beforehand
        def enterControlMode(self):
                print "entering control mode"
                global matrix
                # Save RGB Values
                for i in range (0,64):
                        self.savedMatrixRGB[i] = matrix.getPixelColor(i)
                # Set Brightness Levels
                for i in range (0, self.curLevel.firstLED):
                        matrix.setPixelColor(i, Colors.BLACK)
                for i in range (self.curLevel.firstLED, 64):
                        matrix.setPixelColor(i, self.pixelColor)
                matrix.show()

        # Lamp exits brightness control mode, puts back RGB Values
        def exitControlMode(self):
                global matrix
                # Returns Saved RGB Values
                for i in range (0,64):
                        matrix.setPixelColor(i, self.savedMatrixRGB[i])
                matrix.show()

        #Initialize, gets color from last LED
        def __init__(self):
                global matrix
                self.pixelColor = matrix.getPixelColor(self.END_LED)
                self.initializeArray()
                self.curLevel = self.LEDLevelArray[4]
                self.curIndex = 4


def function():
	pass
	
if __name__ == '__main__':
	# Create NeoPixel object with appropriate configuration.
        global matrix
	matrix = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
	# Intialize the library (must be called once before other functions).
	matrix.begin()
        
        for i in range (0,64):
                matrix.setPixelColor(i, 0xFF0000)

        brightnessControl = BrightnessCtrl()

        matrix.show()

	print ('Press Ctrl-C to quit.')

	brightnessControl.enterControlMode()

	while True:
                value = raw_input("up, down, or exit?")
                if value == "up":
                        brightnessControl.upLevel()
                elif value == "down":
                        brightnessControl.downLevel()
                elif value == "exit":
                        brightnessControl.exitControlMode()
                        break
                else:
                        brightnessControl.exitControlMode()
                        break
	


