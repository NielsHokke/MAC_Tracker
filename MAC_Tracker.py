import csv
import matplotlib.pyplot as plt
import struct

file_path = 'output.csv'

# 1519302005.708943170	ac:bc:32:c6:da:59	-52

def show_MACoverTime():
	x = []
	y = []
	c = []
	Mac_list = []

	data = csv.reader(open(file_path), delimiter='	')
	for row in data:
		MAC_scr = row[1]
		time_stamp = row[0]
		if MAC_scr not in Mac_list:
			Mac_list.append(MAC_scr)
		x.append(time_stamp)
		# print(MAC_scr)
		# print()
		y.append(Mac_list.index(MAC_scr))

		c.append(((float.fromhex(MAC_scr[-2:]) / 0xff), (float.fromhex(MAC_scr[-5:-3]) / 0xff), (float.fromhex(MAC_scr[-8:-6]) / 0xff)))


	plt.scatter(x, y, c=c)
	plt.show()

def show_uniqueMacoverTime():
	y = []
	Mac_list = []

	timeslot = 10
	lastTime = 0.0

	data = csv.reader(open(file_path), delimiter='	')
	for row in data:
		MAC_scr = row[1]
		time_stamp = row[0]

		if lastTime == 0:
			lastTime = float(time_stamp)

		if float(time_stamp) > lastTime + timeslot:
			# print("{} > {} + {}".format(float(time_stamp), lastTime, timeslot))
			y.append(len(Mac_list))
			Mac_list = []
			lastTime = float(time_stamp)

		if MAC_scr not in Mac_list:
			Mac_list.append(MAC_scr)

	print(y)

	plt.plot(range(0, len(y)), y)
	plt.show()


show_MACoverTime()
# show_uniqueMacoverTime()
