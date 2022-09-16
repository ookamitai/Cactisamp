import math

import numpy as np


def splitaudio(data, sr, starttime, endtime):
    s = int(starttime * sr / 1000)
    e = int(endtime * sr / 1000)
    newdata = data[s:e]
    return sr, newdata


# get certain part of the wave file


def apply_fadeout(audio, sr, duration):
    # convert to audio indices (samples)
    audio = np.array(audio)
    length = int(duration / 1000 * sr)
    end = audio.shape[0]
    start = end - length

    # compute fade out curve
    # linear fade
    fade_curve = np.linspace(1.0, 0.0, length)

    # apply the curve
    audio[start:end] = audio[start:end] * fade_curve
    audio = np.ndarray.tolist(audio)
    return audio


def apply_fadein(audio, sr, duration):
    # convert to audio indices (samples)
    audio = np.array(audio)
    length = int(duration / 1000 * sr)
    start = 0
    end = length

    # compute fade out curve
    # linear fade
    fade_curve = np.linspace(0.0, 1.0, length)

    # apply the curve
    audio[start:end] = audio[start:end] * fade_curve
    audio = np.ndarray.tolist(audio)
    return audio


def extendaudiof(data, sr, duration, fade_d):
    data = np.ndarray.tolist(data)
    datatime = len(data) / sr * 1000
    lengtho = fade_d / 1000 * sr
    end = apply_fadeout(data, sr, fade_d)[int(-lengtho) :]
    start = apply_fadein(data, sr, fade_d)[0 : int(lengtho)]
    connect = np.add(end, start)
    newdata = data[0 : int((datatime - fade_d / 1000 * sr))]
    appenddata = data[int(fade_d / 1000 * sr) : int((datatime - fade_d / 1000 * sr))]
    cycles = math.floor(duration / (datatime - fade_d)) + 1
    for i in range(cycles - 1):
        newdata = np.append(newdata, connect)
        newdata = np.append(newdata, appenddata)
    cutdata = splitaudio(newdata, sr, 0, duration)[1]
    return cutdata


def extendaudio(data, sr, duration):
    newdata = data
    datatime = len(data) / sr * 1000
    print(type(datatime))
    cycles = math.floor(duration / datatime) + 1
    for i in range(cycles):
        newdata = np.append(newdata, data)
    cutdata = splitaudio(newdata, sr, 0, duration)[1]
    return cutdata
