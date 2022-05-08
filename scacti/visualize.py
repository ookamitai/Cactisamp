import matplotlib.pyplot as plot
import numpy as np
import wave

# shows the sound waves
def visualize(path: str):

	# reading the audio file
	raw = wave.open(path)
	
	# reads all the frames
	# -1 indicates all or max frames
	signal = raw.readframes(-1)
	signal = np.frombuffer(signal, dtype ="int16")
	
	# gets the frame rate
	f_rate = raw.getframerate()

	# to Plot the x-axis in seconds
	# you need get the frame rate
	# and divide by size of your signal
	# to create a Time Vector
	# spaced linearly with the size
	# of the audio file
	time = np.linspace(
		0, # start
		len(signal) / f_rate,
		num = len(signal)
	)

	# using matplotlib to plot
	# creates a new figure
	return time, signal

def showplot(filepath, listtime, listfrq, listfrqsmo):
	time, signal = visualize(filepath)
	fig, ax1 = plot.subplots()
	ax2 = ax1.twinx()
	l1, = ax2.plot(listtime, listfrq)
	l2, = ax2.plot(listtime, listfrqsmo, color="red")
	l3, = ax1.plot(time, signal, color='orange', alpha=0.4)
	plot.legend(handles=[l1, l2, l3], labels=['Original FRQ', 'Smoothed FRQ', 'Waveform'], loc='lower right')
	plot.show()


