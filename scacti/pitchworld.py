import pyworld as pw
import numpy as np


def getFreq(note, A4=440):
    notes = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']

    octave = int(note[2]) if len(note) == 3 else int(note[1])

    keyNumber = notes.index(note[0:-1])

    if keyNumber < 3:
        keyNumber = keyNumber + 12 + ((octave - 1) * 12) + 1
    else:
        keyNumber = keyNumber + ((octave - 1) * 12) + 1

    return A4 * 2 ** ((keyNumber - 49) / 12)

def resynth(x, fs, listfrq, listtime, stepsize, notepitch, targetpitchlist):
    listfrqnew = targetpitchlist
    arrayfrq = np.array(listfrq, dtype=np.float64)
    arraytime = np.array(listtime, dtype=np.float64)
    arraypitch = np.array(listfrqnew, dtype=np.float64)
    _sp = pw.cheaptrick(x, arrayfrq, arraytime, fs)
    _ap = pw.d4c(x, arrayfrq, arraytime, fs)
    y = pw.synthesize(arraypitch, _sp, _ap, fs, stepsize)
    return y, fs

def get64(a):
    c = ord(a)
    if c >= ord("0") and c <= ord("9"):
        return c - ord("0") + 52
    elif c >= ord("A") and c <= ord("Z"):
        return c - ord("A")
    elif c >= ord("a") and c <= ord("z"):
        return c - ord("a") + 26
    elif c == ord("+"):
        return 62
    elif c == ord("/"):
        return 63
    else:
        return 0

def decodepitch(x,y):
    ans = get64(x) * 64 + get64(y)
    if ans > 2047:
        ans = ans -4096
    return ans

def processpitch(pitchstr, notelength, stepsize):
    pitch_split = pitchstr.split("#")
    only_pitch_list = pitch_split[0::2]
    cycle_count_list = pitch_split[1::2]
    if len(cycle_count_list) < len(only_pitch_list):
        for i in range(len(only_pitch_list) - len(cycle_count_list)):
            cycle_count_list.append("0")
    group_pitch_list = []
    convert_pitch_list = []
    used_pitch_list = []
    for i in range(len(only_pitch_list)):
        split_pitch_list = []
        for pitchitem in range(0, len(only_pitch_list[i]), 2):
            split_pitch_list.append(only_pitch_list[i][pitchitem: pitchitem + 2])
        group_pitch_list.append(split_pitch_list)
    for k in range(len(group_pitch_list)):
        for groupitem in group_pitch_list[k]:
            convert_pitch_list.append(decodepitch(groupitem[0],groupitem[1]))
        for timeitem in cycle_count_list:
            convert_pitch_list.append(convert_pitch_list[-1])

    pitch_dict = {}
    every_pitch_duration = notelength / len(convert_pitch_list)
    for q in range(len(convert_pitch_list)):
        pitch_dict.update({convert_pitch_list[q]:every_pitch_duration*(q)})
    print(pitch_dict)
    target_pitch_count = notelength / stepsize
    for j in range(round(target_pitch_count)-2):
        if pitch_dict.get(convert_pitch_list[j]) <= stepsize*(j+1) <= pitch_dict.get(convert_pitch_list[j+1]):
            diff_pitch = convert_pitch_list[j+1] - convert_pitch_list[j]
            pitch_unit = diff_pitch / every_pitch_duration
            fixed_pitch = convert_pitch_list[j] + pitch_unit * (stepsize*j- pitch_dict.get(convert_pitch_list[j]))
            used_pitch_list.append(fixed_pitch)
        #print(len(used_pitch_list))

    return used_pitch_list

#print(processpitch("6T6o7B7b718M8g8u82828w8k8S757U6j5s4x31262B1K0YzqzAycx/xnxVxMxTx2ywz81X254d577O8O859M9N9O9Q9T9W9Z9c9f9h9i9i9g9a9Q9D818m8Y8N8E7/7/8J8d869c+C+n/J/k/3//AA#14#/8/h+v9s8e7O6D5G4d4M#18#", 950, 10))

