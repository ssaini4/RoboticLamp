import time
import os

#Must install MP4Box with "sudo apt-get install -y gpac"

"Process time must be under 150ms."

start_time = time.time()

print "Taking 10 second video..."

os.system("raspivid -t 10000 -w 320 -h 240 -fps 12  -o controlRV1video.h264")

process_time = time.time() - start_time - 10

if process_time <= 0.35:
	print "Process time was " + str(process_time * 100)+ "ms. PASSED"
else:
	print "Process time was " + str(process_time * 100)+ "ms. FAILED"

choice = raw_input("Check video output? y or n - ")

if choice == "y":
	os.system("MP4Box -add controlRV1video.h264 mp4out.mp4")
	os.system("open mp4out.mp4")

os.system("rm controlRV1video.h264 mp4out.mp4")
