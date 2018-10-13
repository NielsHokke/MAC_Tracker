import time
import os

while True:
	min = round( time.time()/60 - 0.5)%5
	if min == 0:
		filename = time.strftime("%H-%M-%S.mkv")
		print(filename)
		os.system('ffmpeg -i /dev/video0 -t 60 ' + filename)
		time.sleep(90)
	time.sleep(1)

