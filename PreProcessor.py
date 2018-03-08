from tkinter import ttk
import tkinter
import csv
import collections
import datetime

declutter_min = 0.0         # The minimum amount of seconds an MAC must have been away to be able to be registered again
declutter_max = 300000.0    # If a MAC is continuously deleted because of above plot a point every X seconds
min_occurence = 0           # Only output Mac entries that have been seen more than this number
max_occurence = 9999999       # ONly output mac entries that have been seen less than this number
Ignore_Singletons = True    # if True Mac addresses that only appear once are deleted from the results

starts_with = "94:65:2d:2d:14:17"

useMAClist = True           # If enabled only MAC addresses from the list on the next line will be outputted
Special_MAC = {'Niels': '94:65:2d:2d:14:17',
			   'Jetse': '34:80:b3:f0:30:69',
			   'rand1': '9c:f4:8e:17:4c:bd',
			   'rand2': '1',
			   'rand3': '1',
			   'rand4': '1',
			   'rand5': '1',
			   'rand6': '1',
			   'rand7': '1',
			   'rand8': '1'}

input_file = 'measurments/Total.csv'
output_file = 'measurments/Output.csv'


#GUI for creating a tree view of all the entries, their occurences and the last time they're seen
class GuiTracker:
	def __init__(self, myParent, MACtionary):

		self.myContainer = tkinter.ttk.Frame(myParent)

		self.tree = tkinter.ttk.Treeview(self.myContainer, height="25")

		self.tree["columns"]=("one","two")
		self.tree.column("one", width=100)
		self.tree.column("two", width=200)
		self.tree.heading("one", text="Occurrences")
		self.tree.heading("two", text="Last time seen")

		for MAC in MACtionary:
			# print(MAC, len(MACtionary[MAC]))
			Parent = self.tree.insert("", "end", text=MAC, values=(len(MACtionary[MAC]), datetime.datetime.fromtimestamp(int(MACtionary[MAC][-1])).strftime('%Y-%m-%d %H:%M:%S')))
			if len(MACtionary[MAC]) > 1:
				for Time in MACtionary[MAC]:
					self.tree.insert(Parent, "end", MAC + str(Time), text=" " + MAC , values=(" ", datetime.datetime.fromtimestamp(int(Time)).strftime('%Y-%m-%d %H:%M:%S')))
		self.myContainer.pack()

		self.tree.pack(side="left")

		self.scrollbar = ttk.Scrollbar(self.myContainer, command=self.tree.yview)
		self.scrollbar.pack(side="right", fill="y")

		self.tree.configure(yscrollcommand=self.scrollbar.set)


macaskey = {}

# Read the CSV file and create a dict with the mac as key's to quickly
readlines = 0
with open(input_file, newline='') as csvfile:
	spamreader = csv.reader(csvfile, delimiter='\t')
	for row in spamreader:
		readlines = readlines + 1
		if float(row[0]) < 1519711200:
			continue
		if row[1] in Special_MAC.values() or not useMAClist:
			if not row[1] in macaskey:
				macaskey.update({row[1]:[]})

			if (len(macaskey[row[1]])) > 1:
				if ((float(row[0]) - macaskey[row[1]][-1]) < declutter_min) and (macaskey[row[1]][-1] - macaskey[row[1]][-2] < declutter_max):
					macaskey[row[1]][-1] = float(row[0])
				else:
					macaskey[row[1]].append(float(row[0]))
			else:
				macaskey[row[1]].append(float(row[0]))


macstoremove= []
for MAC in macaskey:
	if len(macaskey[MAC]) == 2 and ((macaskey[MAC][1] - macaskey[MAC][0]) < declutter_min):  # and Ignore_Singletons:
		macaskey[MAC].pop()
	if (len(macaskey[MAC])== 1 and Ignore_Singletons) or len(macaskey[MAC]) < min_occurence or len(macaskey[MAC]) > max_occurence:
		macstoremove.append(MAC)

for MAC in macstoremove:
	macaskey.pop(MAC)

# Helper dict to easily sort entries on arrival time before outputting
timeaskey = {}
for MAC in macaskey:
	if not (len(macaskey[MAC]) <= 1 and Ignore_Singletons):
		for time in macaskey[MAC]:
			timeaskey.update({time: MAC})

ordereddict = collections.OrderedDict(sorted(timeaskey.items()))

# CSV write
writelines = 0
with open(output_file, 'w', newline='') as csv_file:
	writer = csv.writer(csv_file, delimiter='\t')
	for key, value in ordereddict.items():
		writelines = writelines + 1
		writer.writerow([key, value])

print("Reduce from " + str(readlines) + " data points to " + str(writelines) + " lines")

# Display the interface
# root = tkinter.Tk()
# root.resizable(False, False)
# application = GuiTracker(root, macaskey)
#
# root.mainloop()


