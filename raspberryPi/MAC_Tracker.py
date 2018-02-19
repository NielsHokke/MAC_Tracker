import subprocess
import threading
import time
import os
from os import listdir
from os.path import isfile, join

print("starting")

interface = "wlan0"
duration = 300
file_prefix = "data"
capture_filter = "not subtype beacon"
output_dir = "output"

def sniffer():
    cmd1 = "airmon-ng check kill"
    cmd2 = "airmon-ng start " + interface
    cmd3 = "tshark -i " + interface  + "mon -b duration:" + str(duration)  + " -w " + file_prefix
    filter = [capture_filter]

    process = subprocess.Popen(cmd1.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    #print(output)
    #print(error)

    process = subprocess.Popen(cmd2.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    #print(output)
    #print(error)

    cmd3 = cmd3.split()
    cmd3.extend(filter)
    process = subprocess.Popen(cmd3, stdout=subprocess.PIPE)
    output, error = process.communicate()
    #print(output)
    #print(error)

def zipper():
    cmd6 = "mkdir " + output_dir
    process = subprocess.Popen(cmd6.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
	
	#TODO mount USB-stick

    while True:
        this_path = os.path.dirname(os.path.abspath('__file__'))
        file_list = [f for f in listdir(this_path) if isfile(join(this_path, f))]

        data_files = []
        for file in file_list:
            if file_prefix in file:
                data_files.append(file)

        data_files = sorted(data_files)
        if len(data_files) >= 2:
            print("Zipping", data_files[0])
            cmd4 = "tar -czvf " + output_dir  + "/" + data_files[0]
            cmd4 += ".tar.gz " + data_files[0]
            process = subprocess.Popen(cmd4.split(), stdout=subprocess.PIPE)
            output, error = process.communicate()

            cmd5 = "rm "
            cmd5 += data_files[0]
            process = subprocess.Popen(cmd5.split(), stdout=subprocess.PIPE)
            output, error = process.communicate()


        #print(file_list)
        time.sleep(duration/2)

sniffer_thread = threading.Thread(target=sniffer)
zipper_thread = threading.Thread(target=zipper)

sniffer_thread.start()
zipper_thread.start()
