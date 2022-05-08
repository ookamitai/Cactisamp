print("Plz wait...")
import crepe
from scipy.io import wavfile
import os
from pathlib import Path as pathlibpath
import numpy
from scipy.signal import savgol_filter
import time as timeprocess
import gui


os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

def readconfig(configpath):
    with open(configpath, "r", encoding='utf-8') as configfile:
        for line in configfile:
            # print(line)
            # go through every line
            if line.startswith("stepsize="):
                stepsize = int(line.replace("stepsize=", "").replace("\n", ""))
            if line.startswith("modelcapacity="):
                modelcapacity = line.replace("modelcapacity=", "").replace("\n", "")
            if line.startswith("windowsize="):
                windowsize = int(line.replace("windowsize=", "").replace("\n", ""))
            if line.startswith("polyorder="):
                polyorder = int(line.replace("polyorder=", "").replace("\n", ""))
            if line.startswith("frqtype="):
                frqtype = int(line.replace("frqtype=", "").replace("\n", ""))
            if line.startswith("debug="):
                debugvalue = int(line.replace("debug=", "").replace("\n", ""))
    return stepsize, modelcapacity, windowsize, polyorder, frqtype, debugvalue


def getPitch(inputpath, configpath):
    startTime = timeprocess.time()
    stepsize, modelcapacity, windowsize, polyorder = readconfig(configpath)[0:4]
    debugvalue = readconfig(configpath)[5]
    # read config
    sr, audio = wavfile.read(inputpath)
    # read wave file
    time, frequency, confidence, activation = crepe.predict(audio, sr, viterbi=False, step_size=stepsize,
                                                            model_capacity=modelcapacity)
    # use crepe for f0 estimation
    listtime, listfrq = numpy.ndarray.tolist(time), numpy.ndarray.tolist(frequency)
    listfrqsmo = numpy.ndarray.tolist(savgol_filter(listfrq, windowsize, polyorder))
    # convert float64 to list
    print('Analysis time: ', timeprocess.time() - startTime, "s", sep='')
    # print time
    return inputpath, stepsize, listtime, listfrq, listfrqsmo


def writetoFile(path, stepsize, time, frq, smooth):
    outpath = os.path.dirname(path) + '/' + pathlibpath(path).stem + '.cacti'
    # define cacti file path
    print(outpath)
    # print it
    with open(outpath, 'w', encoding='utf-8') as file:
        # open the file and write data
        file.write("ver=b0.1" + '\n')
        file.write("stepsize=")
        file.write(str(stepsize) + '\n')
        file.write("time=")
        file.write(str(time) + '\n')
        file.write("frq=")
        file.write(str(frq) + '\n')
        file.write("smo=")
        file.write(str(smooth) + '\n')

#for testing purposes...
#run this script directly to test it

if __name__ == "__main__":
    if os.path.exists('cacticonfig.txt') == False:
        print("Cannot read from cacticonfig.txt")
        input()
        exit()
    print("Cacti Utility.")
    #use pyGUI for ... maybe path selection?
    #cuz' drag 'n drop feature didn't work well becaused of format
    while True:
        try:
            foldername, fnames = gui.guiwindow()
            break
        except TypeError:
            print("No folder selected!")
    print(foldername)
    print(len(fnames), "files found.")
    c = 0
    starttime = timeprocess.time()
    for filename in fnames:
        c = c + 1
        targetfilepath = os.path.join(foldername, filename)
        if os.path.isfile(targetfilepath):
            #print(targetfilepath)
            targetfilepath, stepsize, listtime, listfrq, listfrqsmo = getPitch(os.path.join(foldername, filename),'cacticonfig.txt')
            writetoFile(targetfilepath, stepsize, listtime, listfrq, listfrqsmo)
            print(c, "/", len(fnames), " ", round(c/len(fnames)*100, 3),"%",sep="")
    print(timeprocess.time() - starttime)
    print("Finished.")
    input()
    exit()
