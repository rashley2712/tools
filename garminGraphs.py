#!/usr/bin/env python3

import argparse, numpy
import datetime
import sys
import os
import json
from xml.dom import minidom
import matplotlib.pyplot

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Reads a .TCS file from Garmin and plots things.')
	parser.add_argument('inputFile', type=str, help="Name of the .tcx file.")
	
	arg = parser.parse_args()

	xmldoc = minidom.parse(arg.inputFile)
	trackPoints = xmldoc.getElementsByTagName('Trackpoint')
	print("%d trackpoints in %s"%(len(trackPoints), arg.inputFile))
	
	data = []
	
	count = 0
	shortPoints = [trackPoints[0], trackPoints[1]]
	for t in trackPoints:
		count+=1
		dataPoint = {}
		#print(t.childNodes)
		try:
			timeNode = t.getElementsByTagName('Time')
			heartNode = t.getElementsByTagName('HeartRateBpm').item(0).getElementsByTagName('Value')
			dataPoint['time'] = timeNode[0].firstChild.nodeValue
			dataPoint['BPM'] = int(heartNode[0].firstChild.nodeValue)
			print(dataPoint['time'], dataPoint['BPM'])
			data.append(dataPoint)
		except:
			print("Could not find some data in trackPoint number %d"%count)


	for d in data:
		d['date'] = datetime.datetime.strptime(d['time'], "%Y-%m-%dT%H:%M:%S.%fZ")
	
	startDate = data[0]['date']
	for d in data:
		timeSince = ((d['date'] - startDate).seconds) / 60.
		d['minutes'] = float(timeSince)

	# Smooth
	n=300
	for i in range(n):
		data[i]['smoothBPM'] = float('nan')
	for i in range(n, len(data)):
		sum = 0
		for j in range(n):
			sum+= data[i-j]['BPM']
		sum/=n
		data[i]['smoothBPM'] = sum



	

	

	# Write to a CSV file
	fileparts = os.path.splitext(arg.inputFile)
	print(fileparts)
	filename = fileparts[0] + ".csv"
	print("Writing to %s"%filename)
	outputFile = open(filename, 'wt')
	outputFile.write("Date, Minutes since start, BPM\n")
	for d in data:
		outputFile.write("%s, %f, %d\n"%(d['date'], d['minutes'], d['BPM']))
	outputFile.close()
	print(".... file written.")	


	xValues = [ d['date'] for d in data]
	
	
	matplotlib.pyplot.figure(figsize=(12,12/1.6))

	yValues = [ d['BPM'] for d in data]
	print("Mean: %f\nMedian: %f"%(numpy.mean(yValues), numpy.median(yValues)))
	matplotlib.pyplot.step(xValues, yValues, lw=0.75, alpha=0.3)

	yValues = [ d['smoothBPM'] for d in data]
	print("Mean: %f\nMedian: %f"%(numpy.mean(yValues), numpy.median(yValues)))
	matplotlib.pyplot.step(xValues, yValues, lw=2., alpha=1, color = 'g')

	axes = matplotlib.pyplot.gca()

	matplotlib.pyplot.draw()

	matplotlib.pyplot.savefig("chart.pdf")


	matplotlib.pyplot.show()


