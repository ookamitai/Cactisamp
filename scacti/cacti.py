import sys
import os
from pathlib import Path as pathlibpath

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"


def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False


def readconfig(configpath):
    with open(configpath, "r", encoding="utf-8") as configfile:
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


def readcacti(wavpath):
    cactipath = (
        os.path.join(os.path.dirname(wavpath), pathlibpath(wavpath).stem) + ".cacti"
    )
    with open(cactipath, "r", encoding="utf-8") as cactifile:
        # open the cacti file
        for line in cactifile:
            # for every line in the file
            # print(line)
            if line.startswith("ver="):
                version = str(line.replace("ver=", "").replace("\n", ""))
            if line.startswith("stepsize="):
                stepsize = int(line.replace("stepsize=", "").replace("\n", ""))
            if line.startswith("time="):
                listtime = [
                    float(item)
                    for item in line.replace("time=", "")
                    .replace("\n", "")
                    .replace("[", "")
                    .replace("]", "")
                    .split(",")
                ]
            if line.startswith("frq="):
                listfrq = [
                    float(item)
                    for item in line.replace("frq=", "")
                    .replace("\n", "")
                    .replace("[", "")
                    .replace("]", "")
                    .split(",")
                ]
            if line.startswith("smo="):
                listsmo = [
                    float(item)
                    for item in line.replace("smo=", "")
                    .replace("\n", "")
                    .replace("[", "")
                    .replace("]", "")
                    .split(",")
                ]

    return wavpath, stepsize, listtime, listfrq, listsmo, version


# for testing purposes...
# run this script directly to test it

if len(sys.argv) < 11 or len(sys.argv) > 11:
    print("CactiSamp only work as a back-end of UTAU.")
    input()

if len(sys.argv) == 11:
    # resampler input output notekey convel flags filebegin length loopstart loopend pitch
    print(sys.argv)
