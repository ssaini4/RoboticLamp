'''
	Hard-coded Gestures to test integration of
	LEDs and Motors.
'''

import pexpect
import time

NL = '\n'

print ('Press Ctrl-C to quit.')

led = pexpect.spawn('sudo PYTHONPATH=".build/lib.linux-armv6l-2.7" python LEDLogic.py')
print "initializing LEDs."
time.sleep(5)
print "initializing LEDs done."

while True:
	print '''\nWhich Gesture would you like to try?
	0 - Brightness Up
	1 - Brightness Down
	2 - Show Time
	3 - Color Rotation
	'''

	gestureChoice = raw_input("Choice: ")

	if gestureChoice == "0" or gestureChoice == "1":
		prompt = "How many levels?"

	elif gestureChoice == "2":
		prompt = "How many seconds?"

	elif gestureChoice == "3":
		prompt = "How many rotations?"

	else:
		print "Try again.\n"
		continue

	while True:
		try:
			numChoice = raw_input(prompt + " ")
			if int(numChoice):
				break
		except ValueError:
			print "Try again.\n"

	# 1 second for entrance, 1 second per iteration, 1 second for exit
	print "This Gesture will take " + str(2 + numChoice) + " seconds."
	
	# Brightness Up
	if gestureChoice == "0":
		inputStr = "BC.enterControlMode()"
		led.send(inputStr + NL)

		time.sleep(1)

		for i in range (0, numChoice):
			inputStr = "BC.upLevel()"
			led.send(inputStr + NL)

			time.sleep(1)

		inputStr = "BC.exitControlMode()"
		led.send(inputStr + NL)
		time.sleep(1)

	# Brightness Down
	elif gestureChoice == "1":
		inputStr = "BC.enterControlMode()"
		led.send(inputStr + NL)

		time.sleep(1)

		for i in range (0, numChoice):
			inputStr = "BC.downLevel()"
			led.send(inputStr + NL)

			time.sleep(1)

		inputStr = "BC.exitControlMode()"
		led.send(inputStr + NL)
		time.sleep(1)

	# Time Clock
	elif gestureChoice == "2":
		inputStr = "CLK.enterLEDClock()"
		led.send(inputStr + NL)
		time.sleep(1)

		inputStr = "CLK.showTime(" + numChoice + ")"
		led.send(inputStr + NL)
		time.sleep(numChoice)

		inputStr = "CLK.exitLEDClock()"
		led.send(inputStr + NL)
		time.sleep(1)

	# Color Rotation
	elif gestureChoice == "3":
		inputStr = "ROT.enterColorRotator()"
		led.send(inputStr + NL)
		time.sleep(1)

		for i in range (0, numChoice):
			inputStr = "ROT.nextColor()"
			led.send(inputStr + NL)
			time.sleep(1)

		inputStr = "ROT.exitColorRotator()"
		led.send(inputStr + NL)
		time.sleep(1)

	else:
		pass
