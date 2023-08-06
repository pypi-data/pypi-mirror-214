import time
import signal
import sys
import datetime
import matplotlib
import matplotlib.pyplot as plt
import tempfile
import os
import argparse
import numpy as np
import psutil
import math
from matplotlib.ticker import MaxNLocator
from .utils import parseDurationToSecond

matplotlib.use('Agg')

parser = argparse.ArgumentParser()
parser.add_argument('--duration', default='', help='Duration to export the memory usage. Accept format: 30s | 10m | 8h | 1d')
parser.add_argument('--location', default='', help='Location to save the usage log file')

location = tempfile.gettempdir()
if parser.parse_args().location != '':
    location = parser.parse_args().location

currTime = time.time()
memDataFileName = 'mem_visualize_' + str(round(currTime)) + '.txt'
memDataFilePath = os.path.join(location, memDataFileName)

cpuDataFileName = 'cpu_visualize_' + str(round(currTime)) + '.txt'
cpuDataFilePath = os.path.join(location, cpuDataFileName)
startTime = time.time()

def visualizeMemoryData():
    endTime = time.time()
    mem_timestamps = []
    mem_used = []
    mem_free = []
    
    cpu_timestamps = []
    cpu_used = []
    cpu_free = []

    with open(memDataFilePath,'r') as memDataFile:
        for line in memDataFile:
            if "TIMESTAMP" not in line:
                lineSplited = line.strip().split(' ')
                dt_object = datetime.datetime.fromtimestamp(float(lineSplited[0]))
                formatted_time = dt_object.strftime('%H:%M:%S')

                mem_timestamps.append(formatted_time)
                mem_used.append(float(lineSplited[1]))
                mem_free.append(float(lineSplited[2]))

    with open(cpuDataFilePath,'r') as cpuDataFile:
        for line in cpuDataFile:
            if "TIMESTAMP" not in line:
                lineSplited = line.strip().split(' ')
                dt_object = datetime.datetime.fromtimestamp(float(lineSplited[0]))
                formatted_time = dt_object.strftime('%H:%M:%S')

                cpu_timestamps.append(formatted_time)
                cpu_used.append(float(lineSplited[1]))
                cpu_free.append(float(lineSplited[2]))

    ax = plt.subplot(1,2,1)
    ax.stackplot(mem_timestamps, mem_used, mem_free, labels=['Used', 'Free'])
    ax.legend(loc='upper left')
    ax.set_title('Memory usage')
    ax.set_xlabel('Time')
    ax.set_ylabel('MB')
    ax.xaxis.set_major_locator(MaxNLocator(nbins=10))
    ax.tick_params(axis='x', rotation=90)

    ax1 = plt.subplot(1,2,2)
    ax1.stackplot(cpu_timestamps, cpu_used, cpu_free, labels=['Used', 'Free'])
    ax1.legend(loc='upper left')
    ax1.set_title('CPU usage')
    ax1.set_xlabel('Time')
    ax1.set_ylabel('MB')
    ax1.xaxis.set_major_locator(MaxNLocator(nbins=10))
    ax1.tick_params(axis='x', rotation=90)

    dt_object = datetime.datetime.fromtimestamp(startTime)
    formatted_start_time = dt_object.strftime('%Y_%m_%d_%H_%M')
    dt_object = datetime.datetime.fromtimestamp(endTime)
    formatted_end_time = dt_object.strftime('%Y_%m_%d_%H_%M')

    imageFileName = 'HW_' + formatted_start_time + '-' + formatted_end_time + '.png'
    plt.savefig(imageFileName, bbox_inches="tight")
    print('Created graph file:', imageFileName)

def signal_handler(sig, frame):
    print('Process was killed')
    sys.exit(0)

signal.signal(signal.SIGTERM, signal_handler)

def writeHardwareUsageHistory(endTime):    
    print('Writing memory usage history to:', memDataFilePath)
    memDataFile = open(memDataFilePath, "w")
    memDataFile.write('TIMESTAMP USED AVAI\n')

    print('Writing CPU usage history to:', cpuDataFilePath)
    cpuDataFile = open(cpuDataFilePath, "w")
    cpuDataFile.write('TIMESTAMP USED AVAI\n')

    try:
        while True:
            cpu_percent = psutil.cpu_percent(interval=30)

            # Stop if over the endtime
            if endTime > 0:
                if time.time() > endTime:
                    memDataFile.close()
                    cpuDataFile.close()
                    visualizeMemoryData()
                    break

            mem = psutil.virtual_memory()
            available_mem = mem.available / (1024 ** 2)   # convert to MB
            used_mem = (mem.total - mem.available) / (1024 ** 2)

            memDataFile.write(str(round(time.time())) + " ")
            memDataFile.write(str(used_mem) + ' ')
            memDataFile.write(str(available_mem) + ' ')
            memDataFile.write('\n')
            memDataFile.flush()

            cpuDataFile.write(str(round(time.time())) + " ")
            cpuDataFile.write(str(cpu_percent) + ' ')
            cpuDataFile.write(str(100 - cpu_percent) + ' ')
            cpuDataFile.write('\n')
            cpuDataFile.flush()

    except KeyboardInterrupt:
        # User kill process
        memDataFile.close()
        cpuDataFile.close()
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
    
    writeHardwareUsageHistory(endTime)
