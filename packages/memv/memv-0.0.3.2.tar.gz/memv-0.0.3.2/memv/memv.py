import time
import signal
import sys
import datetime
import matplotlib.pyplot as plt
import tempfile
import os
import argparse
import numpy as np
import psutil
from utils import parseDurationToSecond

parser = argparse.ArgumentParser()
parser.add_argument('--duration', default='', help='Duration to export the memory usage. Accept format: 30s | 10m | 8h | 1d')

temDir = tempfile.gettempdir()
memDataFileName = 'mem_visualize_' + str(round(time.time())) + '.txt'
memDataFilePath = os.path.join(temDir, memDataFileName)
startTime = time.time()

def visualizeMemoryData():
    endTime = time.time()
    timestamps = []
    used = []
    free = []

    with open(memDataFilePath,'r') as memDataFile:
        for line in memDataFile:
            if "TIMESTAMP" not in line:
                lineSplited = line.strip().split(' ')
                dt_object = datetime.datetime.fromtimestamp(int(lineSplited[0], 10))
                formatted_time = dt_object.strftime('%H:%M:%S')

                timestamps.append(formatted_time)
                used.append(float(lineSplited[1]))
                free.append(float(lineSplited[2]))

    from matplotlib.ticker import MaxNLocator

    fig, ax = plt.subplots()
    ax.stackplot(timestamps, used, free, labels=['Used', 'Free'])
    ax.legend(loc='upper left')
    ax.set_title('Memory usage')
    ax.set_xlabel('Time')
    ax.set_ylabel('MB')
    ax.xaxis.set_major_locator(MaxNLocator(nbins=10))
    ax.tick_params(axis='x', rotation=90)

    dt_object = datetime.datetime.fromtimestamp(startTime)
    formatted_start_time = dt_object.strftime('%Y_%m_%d_%H:%M')
    dt_object = datetime.datetime.fromtimestamp(endTime)
    formatted_end_time = dt_object.strftime('%Y_%m_%d_%H:%M')

    imageFileName = formatted_start_time + '-' + formatted_end_time + '.png'
    plt.savefig(imageFileName, bbox_inches="tight")
    print('Created graph file:', imageFileName)
    plt.show()

def signal_handler(sig, frame):
    print('Process was killed')
    sys.exit(0)

signal.signal(signal.SIGTERM, signal_handler)

def writeMemUsageHistory(endTime):
    # output: PhysMem: 7585M used (1338M wired), 86M unused.
    command = "top -l 1 -s 0 | grep PhysMem"  # your shell command here
    
    print('Writing memory usage history to:', memDataFilePath)
    dataFile = open(memDataFilePath, "w")
    dataFile.write('TIMESTAMP USED AVAI\n')

    try:
        while True:
            time.sleep(1)
            # Stop if over the endtime
            if endTime > 0:
                if time.time() > endTime:
                    dataFile.close()
                    visualizeMemoryData()
                    break

            mem = psutil.virtual_memory()
            available_mem = mem.available / (1024 ** 2)   # convert to MB
            used_mem = (mem.total - mem.available) / (1024 ** 2)

            dataFile.write(str(round(time.time())) + " ")
            dataFile.write(str(used_mem) + ' ')
            dataFile.write(str(available_mem) + ' ')
            dataFile.write('\n')
            dataFile.flush()
    except KeyboardInterrupt:
        # User kill process
        dataFile.close()
        visualizeMemoryData()

def memv():
    print('Process is running, press "Ctrl + C" to stop!')
    dt_object = datetime.datetime.fromtimestamp(startTime)
    formatted_time = dt_object.strftime('%H:%M:%S')
    print('Startime:', formatted_time)
    args = parser.parse_args()

    endTime = 0
    if args.duration != '':
        duration = parseDurationToSecond(args.duration)
        endTime = startTime + duration
        dt_object = datetime.datetime.fromtimestamp(endTime)
        formatted_time = dt_object.strftime('%H:%M:%S')
        print('Endtime:', formatted_time)
    
    writeMemUsageHistory(endTime)
