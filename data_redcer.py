from tkinter import ttk
import tkinter
import csv
import collections

declutter_min = 3600.0
declutter_max = 300000.0
Ignore_Singletons = True

input_file = 'measurments/dinsdagwoensdagfixed.csv'
output_file = 'dinsdagwoensdag.csv'

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
			Parent = self.tree.insert("", "end", text=MAC, values=(len(MACtionary[MAC]), MACtionary[MAC][-1]))
			if len(MACtionary[MAC]) > 1:
				for Time in MACtionary[MAC]:
					self.tree.insert(Parent, "end", MAC + str(Time), text=" " + MAC , values=(" ", Time))
		self.myContainer.pack()

		self.tree.pack(side="left")

		self.scrollbar = ttk.Scrollbar(self.myContainer, command=self.tree.yview)
		self.scrollbar.pack(side="right", fill="y")

		self.tree.configure(yscrollcommand=self.scrollbar.set)


macaskey = {}

readlines = 0
with open(input_file, newline='') as csvfile:
	spamreader = csv.reader(csvfile, delimiter='\t')
	for row in spamreader:
		readlines = readlines + 1
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

	if len(macaskey[MAC]) == 2 and ((macaskey[MAC][1] - macaskey[MAC][0]) < declutter_min): # and Ignore_Singletons:
		macaskey[MAC].pop()
	if len(macaskey[MAC])== 1 and Ignore_Singletons:
		macstoremove.append(MAC)

for MAC in macstoremove:
	macaskey.pop(MAC)

timeaskey = {}
for MAC in macaskey:
	if not (len(macaskey[MAC]) <= 1 and Ignore_Singletons):
		for time in macaskey[MAC]:
			timeaskey.update({time: MAC})


ordereddict = collections.OrderedDict(sorted(timeaskey.items()))


writelines = 0
with open(output_file, 'w', newline='') as csv_file:
	writer = csv.writer(csv_file, delimiter='\t')
	for key, value in ordereddict.items():
		writelines = writelines + 1
		writer.writerow([key, value])

print("Reduce from " + str(readlines) + " data points to " + str(writelines) + " lines")

root = tkinter.Tk()
root.resizable(False, False)
application = GuiTracker(root, macaskey)

root.mainloop()


