from neopixel import *
import Colors

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

        matrix = None

        def initializeArray(self):
                for i in range (0, 9):
                        self.LEDLevelArray[i] = LEDLevel(index = i)

        # Going down a brightness level, set higher level row to BLACK
        def downLevel(self):
                print "downlevel"

                if self.curIndex == 0:
                        print "brightness too low. exiting"
                        return
                
                # global matrix
                for i in range(self.curLevel.firstLED, self.LEDLevelArray[self.curIndex-1].firstLED):
                        self.matrix.setPixelColor(i, Colors.BLACK)

                self.curLevel = self.LEDLevelArray[self.curIndex-1]
                self.curIndex = self.curLevel.myLevel
                self.matrix.setBrightness(self.curLevel.brightnessLevel)
                self.matrix.show()

                        
        # 
        def upLevel(self):
                print "uplevel"

                if self.curIndex == 8:
                        print "brightness too high. exiting"
                        return

                # global matrix

                print self.curLevel.firstLED
                print self.curIndex
                
                for i in range(self.LEDLevelArray[self.curIndex+1].firstLED, self.curLevel.firstLED):
                        self.matrix.setPixelColor(i, self.pixelColor)
                self.curLevel = self.LEDLevelArray[self.curIndex+1]
                self.curIndex = self.curLevel.myLevel
                self.matrix.setBrightness(self.curLevel.brightnessLevel)
                self.matrix.show()
                
        # Lamp enters brightness control mode, saves previous RGB Values beforehand
        def enterControlMode(self):
                print "entering control mode"
                # global matrix
                # Save RGB Values
                for i in range (0,64):
                        self.savedMatrixRGB[i] = self.matrix.getPixelColor(i)
                # Set Brightness Levels
                for i in range (0, self.curLevel.firstLED):
                        self.matrix.setPixelColor(i, Colors.BLACK)
                for i in range (self.curLevel.firstLED, 64):
                        self.matrix.setPixelColor(i, self.pixelColor)
                self.matrix.show()

        # Lamp exits brightness control mode, puts back RGB Values
        def exitControlMode(self):
                # global matrix
                # Returns Saved RGB Values
                for i in range (0,64):
                        self.matrix.setPixelColor(i, self.savedMatrixRGB[i])
                self.matrix.show()

        #Initialize, gets color from last LED
        def __init__(self, matrix):
                # global matrix
                self.matrix = matrix
                self.pixelColor = self.matrix.getPixelColor(self.END_LED)
                self.initializeArray()
                self.curLevel = self.LEDLevelArray[4]
                self.curIndex = 4