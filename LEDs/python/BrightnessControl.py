from neopixel import *
import Colors

class LEDLevel:
	def __init__(index):
		myLevel = i
		firstLED = 64 - (8 * i)
		brightnessLevel = (31 * i)
		
class BrightnessCtrl:

        BEGIN_LED = 0
        END_LED = 63

        # NeoPixel derived Variable
        matrix = None

        # Saved Pixel Color to Imitate
        pixelColor = None

        # Current LEDLevel Class
        curLevel = None

        # Current Brightness Index, [0,8]
        curIndex = None

        # Array [0,8] containing LEDLevel Classes
        LEDLevelArray = [None] * 8

        savedMatrixRGB = []

        def initializeArray():
                for i in range (0, 9):
                        self.LEDLevelArray[i] = LEDLevel(i)

        # Going down a brightness level, set higher level row to BLACK
        def downLevel():
                for i in range(curLevel.firstLED, LEDLevelArray[curIndex-1].firstLED):
                        matrix.setPixelColor(i, Colors.BLACK)
                        self.curLevel = self.LEDLevelArray[curIndex-1]
                        self.curIndex = self.curLevel.myLevel
                        matrix.setBrightness(curLevel.brightnessLevel)
                matrix.show()
                        
        # 
        def upLevel():
                for i in range(LEDLevelArray[curIndex+1].firstLED, curLevel.firstLED):
                        matrix.setPixelColor(i, pixelColor)
                        self.curLevel = self.LEDLevelArray[curIndex+1]
                        self.curIndex = curLevel.myLevel
                        matrix.setBrightness(curLevel.brightnessLevel)
                matrix.show()

        # Lamp enters brightness control mode, saves previous RGB Values beforehand
        def enterControlMode():
                # Save RGB Values
                for i in range (0,64):
                        savedMatrixRGB[i] = matrix.getPixelColor(i)
                # Set Brightness Levels
                for i in range (0, curLevel.firstLED):
                        matrix.setPixelColor(i, Colors.BLACK)
                for i in range (curLevel.firstLED, 64):
                        matrix.setPixelColor(i, pixelColor)

        # Lamp exits brightness control mode, puts back RGB Values
        def exitControlMode():
                # Returns Saved RGB Values
                for i in range (0,64):
                        matrix.setPixelColor(i, savedMatrixRGB[i])

        #Initialize, gets color from last LED
        def __init__(self, matrix):
                self.matrix = matrix
                self.pixelColor = matrix.getPixelColor(self.END_LED)
                self.initializeArray
                print len(self.LEDLevelArray)
                self.curLevel = self.LEDLevelArray[4]
                self.curIndex = 4
