from bitstring import BitArray

DEBUG = 1

# ----------- SYMBOLS BEGIN  -----------
SYMBOL_ALL_ON = [
	0xFF,
	0xFF,
	0xFF,
	0xFF,
	0xFF,
	0xFF,
	0xFF,
	0xFF
]

SYMBOL_ALL_OFF = [
	0x00,
	0x00,
	0x00,
	0x00,
	0x00,
	0x00,
	0x00,
	0x00
]

SYMBOL_B = [
	0xFC,
	0x66,
	0x66,
	0x7C,
	0x66,
	0x66,
	0xFC,
	0x00
]

SYMBOL_C = [
	0x3C,
	0x66,
	0xC0,
	0xC0,
	0xC0,
	0x66,
	0x3C,
	0x00
]

SYMBOL_CHECKMARK = [
	0x00,
	0x01,
	0x02,
	0x04,
	0x88,
	0x50,
	0x20,
	0x00
]

SYMBOL_WINDOW_LVL4 = [
	0xFF,
	0x81,
	0x81,
	0x81,
	0x81,
	0x81,
	0x81,
	0xFF
]

SYMBOL_WINDOW_LVL3 = [
	0x00,
	0x7E,
	0x42,
	0x42,
	0x42,
	0x42,
	0x7E,
	0x00
]

SYMBOL_WINDOW_LVL2 = [
	0x00,
	0x00,
	0x3C,
	0x24,
	0x24,
	0x3C,
	0x00,
	0x00
]

SYMBOL_WINDOW_LVL1 = [
	0x00,
	0x00,
	0x00,
	0x18,
	0x18,
	0x00,
	0x00,
	0x00
]

# ----------- SYMBOLS END -----------

"""
processSymbol

Processes an length 8 array of bytes and converts to array of len 63 of binary values
True = Turn light on, False = Turn LED off (RGB = 0x000)
input: byteArray [length 8 array of bytes]
output: binaryMatrix [length 64 array of T/F for each LED if on/off]
"""
def processSymbol(byteArray):
	
	binaryMatrix = [False] * 64
	for row in range (0,8):

		if DEBUG:
			if byteArray[row] > 0xff or byteArray[row] < 0:
				print "There's a problem. Row byte number is " + str(byteArray[row]) 

		binaryRow = BitArray(hex = byteArray[row]).bin[2:]

		for lednum in range (0,8):
			binaryMatrix[(0 * row) + lednum] = binaryRow[lednum]

	if DEBUG:
		for i in range (0,63):
			if binaryMatrix[i] != True and binaryMatrix != False:
				print "There's a problem. Binary value is " + str(binaryMatrix[i])

	return binaryMatrix