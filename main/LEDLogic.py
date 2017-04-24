import time

from neopixel import *
import Colors
import BrightnessControl as BrightCtrl
import RecognitionEntrance as RecogEntr
import RecognitionMode as RecogMode
import Symbols
import LEDClock as Clock
import ColorRotator

from random import randint

# LED strip configuration:
LED_COUNT      = 64      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 31  # Start Brightness at Level 4
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
PIXEL_COLOR    = None

matrix = None
	
if __name__ == '__main__':
	# Create NeoPixel object with appropriate configuration.
        global matrix
	matrix = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
	# Intialize the library (must be called once before other functions).
	matrix.begin()
        
        Colors.setRandomColor(matrix, Symbols.processSymbol(Symbols.SYMBOL_ALL_ON))

        BC = BrightCtrl.BrightnessCtrl(matrix)
        RE = RecogEntr.RecognitionEntrance(matrix)
        RM = RecogMode.RecognitionMode(matrix)
	CLK = Clock.LEDClock(matrix)
        ROT = ColorRotator.ColorRotator(matrix)

        matrix.show()

	print ('Press Ctrl-C to quit.')

        while True:
                value = raw_input("")
                eval(value)
##                value = raw_input("0: RecogEntr, 1: RecogMode, 2: BrightCtrl, 3: exit - ")
##                
##                #Recognition Entrance
##                if value == "0":
##                        inputBool = False
##                        while not inputBool:
##                                value = raw_input("0: Average RGB, 1: Random RGB - ")
##                                if value == "0":
##                                        RE.enterRecognitionEntrance(average = True)
##                                        inputBool = True
##                                elif value == "1":
##                                        RE.enterRecognitionEntrance(random = True)
##                                        inputBool = True
##                                else:
##                                        print "try again"
##
##                        while True:
##                                value = raw_input("up, down, or exit? - ")
##                                if value == "up":
##                                        outBool = RE.upLevel()
##                                        if outBool:
##                                                print "Reached 100%!"
##
##                                elif value == "down":
##                                        outBool = RE.downLevel()
##                                        if outBool:
##                                                print "Already at 0%!"
##
##                                elif value == "exit":
##                                        RE.exitRecognitionEntrance()
##                                        break
##
##                                else:
##                                        print "Try again."
##                                        
##                #Recognition Mode                        
##                elif value == "1":
##                        inputBool = False
##                        while not inputBool:
##                                value = raw_input("0: Average RGB, 1: Random RGB - ")
##                                if value == "0":
##                                        RM.enterRecognitionMode(average = True)
##                                        inputBool = True
##                                elif value == "1":
##                                        RM.enterRecognitionMode(random = True)
##                                        inputBool = True
##                                else:
##                                        print "try again"
##
##                        while True:
##                                value = raw_input("up, down, symbol, nolock, or exit? - ")
##                                if value == "up":
##                                        outBool = RM.upLevel()
##                                        if outBool:
##                                                print "Reached 100%!"
##
##                                elif value == "down":
##                                        outBool = RM.downLevel()
##                                        if outBool:
##                                                print "Already at 0%!"
##
##                                elif value == "symbol":
##                                        RM.displaySymbol(Symbols.processSymbol(Symbols.SYMBOL_B), randint(0,4))
##
##                                elif value == "nolock":
##                                        RM.noLock()
##
##                                elif value == "exit":
##                                        RM.exitRecognitionMode()
##                                        break
##
##                                else:
##                                        print "Try again."
##
##                #Brightness Control
##                elif value == "2":
##                        BC.enterControlMode()
##                        
##                        while True:
##                                value = raw_input("up, down, or exit? - ")
##
##                                if value == "up":
##                                        BC.upLevel()
##
##                                elif value == "down":
##                                        BC.downLevel()
##
##                                elif value == "exit":
##                                        BC.exitControlMode()
##                                        break
##
##                                else:
##                                        print "Try again (BC)"
##                                        
##                elif value == "3":
##                        print "Exiting. Have a good day!"
##                        break
##                
##                else:
##                        print "Try again. (MainLoop)"

