import csv
import matplotlib.pyplot as plt
import matplotlib.ticker as tck
import datetime as dt
import matplotlib.dates as mdates
import math
from manuf import manuf

file_path = 'total_reduced_selected.csv'

Special_MAC = {'Niels': '94:65:2d:2d:14:17', 'Jetse': '34:80:b3:f0:30:69', 'Mark': 'c0:ee:fb:92:d6:01'}


# function shows MAC occurrences over time in a scatter-plot
# giving each unique MAC address a unique color
def show_MACoverTime():
	x = []
	y = []
	c = []
	s = []
	Mac_list = []

	data = csv.reader(open(file_path), delimiter='	')
	for row in data:
		MAC_scr = row[1][0:8]
		time_stamp = row[0]
		if MAC_scr not in Mac_list:
			Mac_list.append(MAC_scr)

		x.append(dt.datetime.fromtimestamp(int(float(time_stamp))))
		# print(MAC_scr)
		# print()
		y.append(Mac_list.index(MAC_scr))

		if MAC_scr in Special_MAC.values():
			s.append(20)  # 75
		else:
			s.append(20)  # 4

		c.append(((float.fromhex(MAC_scr[-2:]) / 0xff), (float.fromhex(MAC_scr[-5:-3]) / 0xff), (float.fromhex(MAC_scr[-8:-6]) / 0xff)))

	print(len(Mac_list))

	fig, ax = plt.subplots()

	plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%a %d %H:%M:%S'))
	ax.set_xlim([min(x) - dt.timedelta(hours=1), max(x) + dt.timedelta(hours=1)])
	plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=8))
	plt.gca().xaxis.set_minor_locator(mdates.MinuteLocator(interval=60))
	sc = plt.scatter(x, y, c=c, s=s)
	plt.gcf().autofmt_xdate()

	annot = ax.annotate("", xy=(0, 0), xytext=(20, 20), textcoords="offset points",
						bbox=dict(boxstyle="round", fc="w"),
						arrowprops=dict(arrowstyle="->"))
	annot.set_visible(False)

	def update_annot(ind):
		ax.set_title(Mac_list[y[ind['ind'][0]]] + "    " + x[ind['ind'][0]].strftime("%d %H:%M:%S"))

	def hover(event):
		vis = annot.get_visible()
		if event.inaxes == ax:
			cont, ind = sc.contains(event)
			if cont:
				update_annot(ind)
				annot.set_visible(True)
				fig.canvas.draw_idle()
			else:
				if vis:
					annot.set_visible(False)
					fig.canvas.draw_idle()
	#
	fig.canvas.mpl_connect("motion_notify_event", hover)

	plt.show()

# function shows a pie chard of vendor types
def show_vendors():
	sizes = {}
	vendors = {}
	total = 0
	other = 0.032

	data = csv.reader(open(file_path), delimiter='	')
	for row in data:
		MAC_scr = row[1][0:8]
		if MAC_scr in sizes:
			sizes[MAC_scr] += 1
		else:
			sizes[MAC_scr] = 1
		total += 1

	p = manuf.MacParser(update=True)
	for key, value in sizes.items():
		vendor = p.get_manuf(key + ':00:00:00')
		if vendor in vendors:
			vendors[vendor] += value
		else:
			vendors[vendor] = value

	vendors2 = {}
	vendors2["other"] = 0
	for key, value in vendors.items():

		if value < total*other:
			vendors2["other"] += value
		else:
			vendors2[key] = value


	print(len(sizes.values()))

	plt.pie(vendors2.values(), labels=vendors2.keys(), autopct='%1.1f%%', shadow=True, startangle=140)
	plt.show()

# function shows the number of unique MAC occurrences per timeslot in a bar-graph
def show_uniqueMacoverTime():
	y = []
	x = []
	Mac_list = []

	timeslot = 1800
	lastHour = 0.0
	lastTime = 0.0

	data = csv.reader(open(file_path), delimiter='\t')
	for row in data:
		MAC_scr = row[1]
		time_stamp = int(float(row[0]))

		if lastTime == 0.0:
			lastTime = time_stamp - (time_stamp % timeslot)

		if time_stamp > lastTime + timeslot:
			x.append(dt.datetime.fromtimestamp(int(float(lastTime))))
			y.append(len(Mac_list))
			Mac_list = []
			lastTime = lastTime + timeslot

		if MAC_scr not in Mac_list:
			Mac_list.append(MAC_scr)

	# print(y)

	fig, ax = plt.subplots()

	plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%a %d %H:%M:%S')) #
	ax.set_xlim([min(x) - dt.timedelta(hours=1), max(x) + dt.timedelta(hours=1)])
	plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=4))
	plt.gca().xaxis.set_minor_locator(mdates.MinuteLocator(interval=30))
	plt.gcf().autofmt_xdate()

	plt.bar(x, y, width=0.019)  # , align='center'
	plt.show()

# function shows the number of unique MAC occurrences per timeslot in a bar-graph averaged over multple days
def show_uniqueMacoverTimeOneDay():
	y = []
	x = []
	Mac_list = []

	timeslot = 1800
	lastTime = 0.0

	data = csv.reader(open(file_path), delimiter='\t')
	for row in data:
		MAC_scr = row[1]
		time_stamp = int(float(row[0]))

		if lastTime == 0.0:
			lastTime = time_stamp - (time_stamp % timeslot)

		if time_stamp > lastTime + timeslot:
			x.append(dt.datetime.fromtimestamp(int(float(lastTime))))
			y.append(len(Mac_list))
			Mac_list = []
			lastTime = lastTime + timeslot

		if MAC_scr not in Mac_list:
			Mac_list.append(MAC_scr)

	x2 = [dt.datetime(2018, 2, 27, 0, 0, 0) + dt.timedelta(seconds=timeslot*x) for x in range(0, int(86400/timeslot))]
	y2 = [0]*int(86400/timeslot)
	for date, count in zip(x, y):
		if 1520031660 < date.timestamp() < 1520115839:
			hour = date.hour
			minute = date.minute
			index = int(hour*(3600/timeslot) + math.floor(minute*(60/timeslot)))
			y2[index] += count

	fig, ax = plt.subplots()

	plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
	ax.set_xlim([min(x2) - dt.timedelta(hours=0), max(x2) + dt.timedelta(hours=0.5)])
	plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=2))
	plt.gca().xaxis.set_minor_locator(mdates.MinuteLocator(interval=30))
	plt.gcf().autofmt_xdate()

	plt.bar(x2, y2, width=0.018, align='edge')  # , align='center'
	# plt.plot(x, y)
	plt.show()



print("started")
show_MACoverTime()
# show_vendors()
# show_uniqueMacoverTime()
# show_uniqueMacoverTimeOneDay()

