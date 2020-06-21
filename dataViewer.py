#!/usr/bin/env python3
import matplotlib.pyplot
import argparse
import datetime
import numpy
from astropy.timeseries import LombScargle


if __name__ == "__main__":
	
	parser = argparse.ArgumentParser(description='Examines a binary file to help decode the data format.')
	parser.add_argument('file', type=str, help='Input filename.')
	parser.add_argument('-o', '--output', type=str, help="")
	args = parser.parse_args()

	if args.output is None:
		args.output = args.file + "_converted.csv"	
	fileHandle = open(args.file, 'rb')
	data = fileHandle.read()
	fileHandle.close()

	
	for i, d in enumerate(data):
		print(i, ": ",d)


	print("Length is:",len(data))

	O2 = []
	heartRate = []
	times = []
	three = []
	movement = []

	# First two lines (of 5 bytes each) are the date and time
	year = data[3] * 256 + data[2]
	month = data[4]
	day = data[5]
	hour = data[6]
	minute = data[7]
	second = data[8]
	print("Year: ", year, "Month:", month, "Day:", day, " - ", hour, ":", minute, ":", second)  
	decimalString = ""
	for c in range(25):
		decimalString+= str(data[c]) + " : " 
	print(decimalString)
	input()
	count = 0
	for i in range(20, len(data), 5):
		print(i, end=' | ')
		decimalString = ""
		for c in range(5):
			decimalString+= str(data[i+c]) + " : " 
		time = (i-20)/5*2
		print(time, decimalString)
		count+=1
		if data[i]==0 or data[i]==255 or data[i+1]==0 or data[i+1]==255:
			#input("bad data?")
			continue
		times.append(time)
		heartRate.append(data[i])
		three.append(data[i+2])
		movement.append(data[i+3])
		O2.append(data[i+1])
		
	print("%d datapoints read\n%d good datapoints"%(count, len(heartRate)))

	# Write to csv format
	startTime = datetime.datetime(year, month, day, hour, minute, second)
	outfile = open(args.output, "wt")
	outfile.write("time, spO2, pulse, movement\n")
	for t, hr, sp, mv in zip(times, O2, heartRate, movement):
		currentTime = startTime + datetime.timedelta(seconds=t)
		outfile.write("%s, %d, %d, %d\n"%((str(currentTime), sp, hr, mv) ))
	outfile.close()
	print("written to file:", args.output)
	matplotlib.pyplot.figure(figsize=(12,6))
	matplotlib.pyplot.plot(times, heartRate, lw=0.4)
	matplotlib.pyplot.plot(times, O2)
	#matplotlib.pyplot.plot(times, three)
	matplotlib.pyplot.plot(times, movement)
	mean = numpy.mean(O2)
	O2 = [ o-mean for o in O2]
	mean = numpy.mean(heartRate)
	matplotlib.pyplot.figure()
	heartRate = [ h-mean for h in heartRate]
	frequency, power = LombScargle(times, O2).autopower(maximum_frequency=0.2)
	matplotlib.pyplot.plot(frequency, power)
	frequency, power = LombScargle(times, heartRate).autopower(maximum_frequency=0.2)
	matplotlib.pyplot.plot(frequency, power, alpha=0.5)
	matplotlib.pyplot.draw()
	matplotlib.pyplot.show()