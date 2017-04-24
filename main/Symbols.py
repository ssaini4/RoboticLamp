import binascii

DEBUG = 0

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

S_1 = [
	0x18,
	0x18,
	0x38,
	0x18,
	0x18,
	0x18,
	0x7E,
	0x00
]

S_2 = [
	0x3C,
	0x66,
	0x06,
	0x0C,
	0x30,
	0x60,
	0x7E,
	0x00
]

S_5 = [
	0x7E,
	0x60,
	0x7C,
	0x06,
	0x06,
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

# Used for entering recognition mode. Size 5 Array.
# Windows go out to in.
# 0% -> 25% -> 50% -> 75% -> 100%
RECOGNITION_IN_PERCENT = [
	[	0x00, 0x00,
		0x00, 0x00,
		0x00, 0x00,
		0x00, 0x00 ],

	[	0xFF, 0x81,
		0x81, 0x81,
		0x81, 0x81,
		0x81, 0xFF ],

	[	0xFF, 0xFF,
		0xC3, 0xC3,
		0xC3, 0xC3,
		0xFF, 0xFF ],

	[	0xFF, 0xFF,
		0xFF, 0xE7,
		0xE7, 0xFF,
		0xFF, 0xFF ],

	[	0xFF, 0xFF,
		0xFF, 0xFF,
		0xFF, 0xFF,
		0xFF, 0xFF ] 
]

# Same as RECOGNITION_IN but
# Windows go in to out.
RECOGNITION_OUT_PERCENT = [
	[	0x00, 0x00,
		0x00, 0x00,
		0x00, 0x00,
		0x00, 0x00 ],

	[	0x00, 0x00,
		0x00, 0x18,
		0x18, 0x00,
		0x00, 0x00 ],

	[	0x00, 0x00,
		0x3C, 0x3C,
		0x3C, 0x3C,
		0x00, 0x00 ],

	[	0x00, 0x7E,
		0x7E, 0x7E,
		0x7E, 0x7E,
		0x7E, 0x00 ],

	[	0xFF, 0xFF,
		0xFF, 0xFF,
		0xFF, 0xFF,
		0xFF, 0xFF ]
]



# Bar at the bottom of the LEDs
# to indicate 0-25-50-75-100% Lock
# Does not affect other LEDs
PERCENT_BAR = [
	[	0x00, 0x00,
		0x00, 0x00,
		0x00, 0x00,
		0x00, 0x00 ],

	[	0x00, 0x00,
		0x00, 0x00,
		0x00, 0x00,
		0x00, 0xC0 ],

	[	0x00, 0x00,
		0x00, 0x00,
		0x00, 0x00,
		0x00, 0xF0 ],

	[	0x00, 0x00,
		0x00, 0x00,
		0x00, 0x00,
		0x00, 0xFC ],

	[	0x00, 0x00,
		0x00, 0x00,
		0x00, 0x00,
		0x00, 0xFF ]
]

#
COLOR_ROTATOR_SCREEN = [ 0xFB, 0x8B, 0x83, 0x8B, 0xFB, 0x03, 0xFF, 0xFF ]

# colon that shows with Hour
TIME_COLON = [ 0x00, 0x01, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00 ]

# Digits in a 15-bit array
HEX_DIGITS = [
	[	1,1,1,1,0,1,1,0,1,1,0,1,1,1,1	], #0
	[	0,0,1,0,0,1,0,0,1,0,0,1,0,0,1	], #1
	[	1,1,1,0,0,1,1,1,1,1,0,0,1,1,1	], #2
	[	1,1,1,0,0,1,1,1,1,0,0,1,1,1,1	], #3
	[	1,0,1,1,0,1,1,1,1,0,0,1,0,0,1	], #4
	[	1,1,1,1,0,0,1,1,1,0,0,1,1,1,1	], #5
	[	1,1,1,1,0,0,1,1,1,1,0,1,1,1,1	], #6
	[	1,1,1,0,0,1,0,0,1,0,0,1,0,0,1	], #7
	[	1,1,1,1,0,1,1,1,1,1,0,1,1,1,1	], #8
	[	1,1,1,1,0,1,1,1,1,0,0,1,1,1,1	]
]

# 15-bit time mappings that map to LED location 0-64.
# 0: H1, 1: H2, 2: M1, 3: M2
TIME_MAPPINGS = [
	[ 0,1,2,8,9,10,16,17,18,24,25,26,32,33,34 ], #Hour1
	[ 4,5,6,12,13,14,20,21,22,28,29,30,36,37,38 ], #Hour2
	[ 25,26,27,33,34,35,41,42,43,49,50,51,57,58,59 ], #Minute1
	[ 29,30,31,37,38,39,45,46,47,53,54,55,61,62,63 ] #Minute2
]

# ----------- SYMBOLS END -----------

"""
timeBinaryProcessor

Processes 15-bit array for a number and maps it to a 64-bit binaryArray based on Hour1, Hour2, Minute1, or Minute2 (each a 15bit mapper)
input:  int digitChoice (0-9)
		int timeChoice (0=H1,1=H2,2=M1,3=M2) - chooses mapping for time
output: binaryMatrix - 64 bit array of true/false
"""
def timeBinaryProcessor(digit, timeChoice):
	binaryMatrix = [None] * 64

	digitArray = HEX_DIGITS[digit]
	timeMapping = TIME_MAPPINGS[timeChoice]

	for lednum in range(0, 64):
		binaryMatrix[lednum] = False

	for binLoc in range(0, len(digitArray)):
		binaryMatrix[timeMapping[binLoc]] = bool(digitArray[binLoc])
                
	return binaryMatrix


"""
binaryMatrixAdder

Adds an array of binaryMatrix - if a bit for an LED location is true for any of them, set to high
input:	binaryMatrices[] - array of binary Matrixes
output: binaryMatrix - Single binaryMatrix after adding binary Matrices
"""
def binaryMatrixAdder(matrices):
	finalBinaryMatrix = [None] * 64
        
	for lednum in range (0,64):
		finalBinaryMatrix[lednum] = False

		for matrixNum in range (0, len(matrices)):
			if matrices[matrixNum][lednum]:
				finalBinaryMatrix[lednum] = True
				break

	return finalBinaryMatrix

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

                if byteArray[row] != None:
                        binaryRow = bin(byteArray[row])[2:].zfill(8)
                        for lednum in range (0,8):
                                binaryMatrix[(8 * row) + lednum] = bool(int(binaryRow[lednum]))
                else:
                        for lednum in range (0,8):
                                binaryMatrix[(8 * row) + lednum] = None

			#print str((0 * row) + lednum) + " " + str(binaryMatrix[(0 * row) + lednum]) + str(binaryRow[lednum])

	if DEBUG:
		for i in range (0,64):
			if binaryMatrix[i] != True and binaryMatrix[i] != False:
				print "There's a problem. Binary value is " + str(bool(binaryMatrix[i]))

	return binaryMatrix
