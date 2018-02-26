import csv
import pprint
from collections import defaultdict
import datetime
import pandas as pd
import os
import time
import matplotlib.pyplot as plt

# path_of_files='C:\\Users\\Nelis\\Dropbox\\1-School\\1-Embedded\\Master\\Q3\\Wireless Networking\\output_power_bank_csv'
path_of_files='output.csv'
day_in_week = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

d = defaultdict(list)
x = defaultdict(list)
y = defaultdict(list)

point_counter = 0

min_dateTime = datetime.datetime(2020, 1, 1)
max_dateTime = datetime.datetime(2000, 1, 1)

seconds = 600
temp_mac_list = []
MAC_list = {}
last = 0

for root, dirs, filenames in os.walk(path_of_files):
	for f in filenames:
		if "data_" in f and not "\\\\\\\\" in f:
			file_name = f

			# year = int(file_name[11:15])
			# month = int(file_name[15:17])
			# day = int(file_name[17:19])
			# hour = int(file_name[19:21])
			# minute = int(file_name[21:23])
			# second = int(file_name[23:25])

			# file_time_offset = datetime.datetime(year, month, day, hour, minute, second)

			try:
				data = csv.reader(open(path_of_files + "\\" + file_name))
				print(path_of_files + "\\" + file_name)
				# skip header in csv
				# next(data)
				for row in data:
					# date_time = (file_time_offset + datetime.timedelta(0, float(row[1])))

					# print(row[0])
					# print(row[1])
					# print(row[2])

					# "Dec 14, 2017 22:11:40.408120741 UTC,"
					year = 2018
					month = 2
					day = int(row[0][4:])
					hour = int(row[1][6:8])
					minute = int(row[1][9:11])
					second = int(row[1][12:14])

					# print(row)
					# print(year, month, day, hour, minute, second)

					date_time = datetime.datetime(year, month, day, hour, minute, second)
					day_date_time = day_in_week[datetime.datetime.today().weekday()] + " " + date_time.isoformat(' ')
					MAC_scr = row[2][0:17]
					if not MAC_scr == '':
						min_dateTime = min(min_dateTime, date_time)
						max_dateTime = max(max_dateTime, date_time)

						# timestamp = int(time.mktime(date_time.timetuple()))

						# d[MAC_scr].append(day_date_time)
						x[MAC_scr].append(date_time)
						y[MAC_scr].append(list(x.keys()).index(MAC_scr))

			except Exception as e:
					print(Exception)


pp = pprint.PrettyPrinter(indent=4)
pp.pprint(MAC_list)


# make up some data
# x = [datetime.datetime.now() + datetime.timedelta(hours=i) for i in range(12)]
# y = [i+random.gauss(0,1) for i,_ in enumerate(x)]


# plot
plt.plot(x,y)
# beautify the x-labels
plt.gcf().autofmt_xdate()

plt.show()



# # x = range(int(time.mktime(min_dateTime.timetuple())), int(time.mktime(max_dateTime.timetuple())))
# x = range(0,len(y))
# print(len(x))
# print(len(y))


# y = [i+random.gauss(0,1) for i,_ in enumerate(x)]
#
# x = range(int(time.mktime(max_dateTime.timetuple())), int(time.mktime(min_dateTime.timetuple())))
#
fig = plt.figure()
ax1 = fig.add_subplot(111)

# ax1.scatter(x, y, s=10, c='b', marker="s", label='first')
# counter = 1
# for (k,v), (k2,v2) in zip(x.items(), y.items()):
# 	ax1.scatter(v, v2, s=10, c='r', marker="o", label=k)

print(type(MAC_list))
print(type(range(0, len(MAC_list))))
lijst = []
for value in MAC_list.values():
	lijst.append(value)

ax1.plot(range(0, len(MAC_list)), lijst)

# plt.legend(loc='upper left')
plt.show()

# x = [datetime.datetime.now() + datetime.timedelta(hours=i) for i in range(12)]
# y = [i+random.gauss(0,1) for i,_ in enumerate(x)]
# plt.scatter(x,y)
