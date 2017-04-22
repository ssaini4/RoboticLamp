from PIL import Image
import os
import time

sizecheck = "sizefile.jpg"

os.system("raspistill -o " + sizecheck + " -w 320 -h 240")

sizeimage = Image.open(sizecheck)

if sizeimage.size == (320,240):
	print "Size Check SUCCEEDED. Image is " + sizeimage.size

else:
	print "Size Check FAILED. Image is " + sizeimage.size

start_time = time.time()

print "taking 100 photos"

for i in range (0,100):
	os.system("raspistill -o " + sizecheck + " -w 320 -h 240")

elapsed_time = start_time - time.time()

if elapsed_time <= 8.333333:
	print "100 photos in " + elapsed_time + " s. PASSED"

else:
	print "100 photos in " + elapsed_time + " s. FAILED"
