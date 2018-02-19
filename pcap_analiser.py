import csv
import pprint
from collections import defaultdict
import datetime
import os

path_of_files='C:\\Users\\Nelis\\Dropbox\\1-School\\1-Embedded\\Master\\Q3\\Wireless Networking\\output_power_bank_csv'


d = defaultdict(list)


for root, dirs, filenames in os.walk(path_of_files):
	for f in filenames:
		file_name = f

		year = int(file_name[11:15])
		month = int(file_name[15:17])
		day = int(file_name[17:19])
		hour = int(file_name[19:21])
		minute = int(file_name[21:23])
		second = int(file_name[23:25])

		file_time_offset = datetime.datetime(year, month, day, hour, minute, second)

		data = csv.reader(open(path_of_files + "\\" + file_name))
		print(path_of_files + "\\" + file_name)
		# skip header in csv
		next(data)
		for row in data:
			time = (file_time_offset + datetime.timedelta(0, float(row[1])))
			time = time.isoformat(' ')
			MAC_scr = row[2][0:17]
			if not MAC_scr == '':
				d[MAC_scr].append(time)


pp = pprint.PrettyPrinter(indent=2)
pp.pprint(d)


