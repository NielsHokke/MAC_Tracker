import csv
import matplotlib.pyplot as plt
import datetime as dt
import matplotlib.dates as mdates
from matplotlib.dates import DayLocator, HourLocator, DateFormatter, drange
import struct
import numpy as np

file_path = 'dinsdagwoensdag.csv'

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

		x.append(dt.datetime.fromtimestamp(int(float(time_stamp))))
		# print(MAC_scr)
		# print()
		y.append(Mac_list.index(MAC_scr))

		c.append(((float.fromhex(MAC_scr[-2:]) / 0xff), (float.fromhex(MAC_scr[-5:-3]) / 0xff), (float.fromhex(MAC_scr[-8:-6]) / 0xff)))

	fig, ax = plt.subplots()

	plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d %H:%M:%S'))
	ax.set_xlim([min(x) - dt.timedelta(hours=1), max(x) + dt.timedelta(hours=1)])
	plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=2))
	plt.gca().xaxis.set_minor_locator(mdates.MinuteLocator(interval=15))
	sc = plt.scatter(x, y, c=c)
	plt.gcf().autofmt_xdate()

	annot = ax.annotate("", xy=(0, 0), xytext=(20, 20), textcoords="offset points",
						bbox=dict(boxstyle="round", fc="w"),
						arrowprops=dict(arrowstyle="->"))
	annot.set_visible(False)

	norm = plt.Normalize(1, 4)
	cmap = plt.cm.RdYlGn

	def update_annot(ind):
		pass
		# print(ind['ind'][0])
		# print(Mac_list[ind['ind'][0]])
		# pos = sc.get_offsets()[ind["ind"][0]]
		# annot.xy = pos
		# text = "{}".format(Mac_list[ind['ind'][0]])
		# annot.set_text(text)
		# annot.get_bbox_patch().set_facecolor(cmap(norm(c[ind["ind"][0]])))
		# annot.get_bbox_patch().set_alpha(0.4)

	def hover(event):
		vis = annot.get_visible()
		if event.inaxes == ax:
			cont, ind = sc.contains(event)
			if cont:
				print(ind)
				update_annot(ind)
				annot.set_visible(True)
				fig.canvas.draw_idle()
			else:
				if vis:
					annot.set_visible(False)
					fig.canvas.draw_idle()
	#
	fig.canvas.mpl_connect("motion_notify_event", hover)

	print(min(x))
	print(max(x))
	# plt.xticks(np.arange(0, 5, 1))
	plt.show()




def show_uniqueMacoverTime():
	y = []
	x = []
	Mac_list = []

	timeslot = 1800
	lastTime = 0.0

	data = csv.reader(open(file_path), delimiter='\t')
	for row in data:
		MAC_scr = row[1]
		time_stamp = row[0]

		if lastTime == 0:
			lastTime = float(time_stamp)

		if float(time_stamp) > lastTime + timeslot:
			# print("{} > {} + {}".format(float(time_stamp), lastTime, timeslot))
			y.append(len(Mac_list))
			x.append(dt.datetime.fromtimestamp(int(float(time_stamp))))
			Mac_list = []
			lastTime = float(time_stamp)

		if MAC_scr not in Mac_list:
			Mac_list.append(MAC_scr)

	# print(y)

	fig, ax = plt.subplots()

	plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d %H:%M:%S'))
	ax.set_xlim([min(x) - dt.timedelta(hours=1), max(x) + dt.timedelta(hours=1)])
	plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=2))
	plt.gca().xaxis.set_minor_locator(mdates.MinuteLocator(interval=15))
	plt.gcf().autofmt_xdate()

	# plt.bar(x, y, width=0.03, align='center')
	plt.plot(x, y)
	plt.show()


show_MACoverTime()
# show_uniqueMacoverTime()
