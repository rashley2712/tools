#!/usr/bin/env python

import requests
import json
import argparse
import time, datetime
import math
import sys
import ppgplot

token = "c9d29aebfd2a9c0150fdab6ad4d614b72568cee8e12ad1994a8421b12021fd58"

headers = {
    "Authorization": "Bearer %s" % token,
}

def sinecurve(time, period):
	periodSeconds = period * 60.
	omega = 2*math.pi/periodSeconds
	return 0.5 + 0.5 * math.sin(omega*time) + 0.2 * math.sin(3*omega*time)

class lightCurve:
	def __init__(self):
		self.time = []
		self.brightness = []
		self.period = 0
		self.numPoints = 0

	def initValues(self, time, brightness):
		if len(time) != len(brightness):
			return -1
		self.time = time
		self.brightness = brightness
		self.numPoints = len(time)
		
		return self.numPoints  

if __name__ == "__main__":

	parser = argparse.ArgumentParser(description='Downloads email list and puts it into a Google doc.')
	parser.add_argument('--test', action='store_true', help='Use the test URL instead of the real URL.')	
	arg = parser.parse_args()
	response = requests.get('https://api.lifx.com/v1beta1/lights/all', headers=headers)

	bulbs = json.loads(response.text)

	print len(bulbs), "bulbs are registered."

	numPoints = 60
	period = .6
	seconds = 0
	step = period * 60. / numPoints
	times = []
	brightness = []
	for x in range(numPoints):
		times.append(seconds)
		brightness.append(sinecurve(seconds, period))
		seconds+= step
	
	lightCurve = lightCurve()
	lightCurve.initValues(times, brightness)
	lightCurve.period = period * 60.
	
	lightCurve.brightness[3] = 1.0
	
	lightCurvePlot = {}
	lightCurvePlot['pgplotHandle'] = ppgplot.pgopen('/xs')
	ppgplot.pgpap(8, 0.618)
	ppgplot.pgenv(0., lightCurve.period, 0.0, 1.0, 0, 0)
	ppgplot.pglab("seconds", "brightness", "Light curve")
	ppgplot.pgpt(lightCurve.time, lightCurve.brightness, 2)
	ppgplot.pgsci(2)
	ppgplot.pgline(lightCurve.time, lightCurve.brightness)
	ppgplot.pgask(False)
	
	connectedCount = 0
	connectedBulbs = []
	for b in bulbs:
		if b['connected'] == True:
			connectedCount+= 1
			connectedBulbs.append(b)
			print b['label'], "is connected!"
			
	print "Number of connected bulbs", connectedCount

	params = {
		"color": "kelvin:2700",
		"power": "on",
		"brightness:":"0"
		}
	response = requests.put("https://api.lifx.com/v1beta1/lights/all/state", headers=headers, params=params)
	time.sleep(3)
	
	for p in range(500):
		for n in range(lightCurve.numPoints):
			if n == lightCurve.numPoints-1:
				timeToNextStep =  lightCurve.period - lightCurve.time[n]
			else:
				timeToNextStep = lightCurve.time[n+1] - lightCurve.time[n]
			
			print n, lightCurve.time[n], lightCurve.brightness[n], timeToNextStep
			ppgplot.pgeras()
			ppgplot.pgsci(1)
			ppgplot.pgenv(0., lightCurve.period, 0.0, 1.0, 0, 0)
			ppgplot.pglab("seconds", "brightness", "Light curve")
			ppgplot.pgpt(lightCurve.time, lightCurve.brightness, 2)
			ppgplot.pgsci(2)
			ppgplot.pgline(lightCurve.time, lightCurve.brightness)
			ppgplot.pgsci(3)
			ppgplot.pgpt([lightCurve.time[n]], [lightCurve.brightness[n]], 3)
			currentLineStyle = ppgplot.pgqls()
			ppgplot.pgsls(2)
			ppgplot.pgline([lightCurve.time[n], lightCurve.time[n]], [ 0, 1])
			ppgplot.pgsls(currentLineStyle)
			
			
			params = {"brightness": str(lightCurve.brightness[n]), "duration": str(timeToNextStep)}
			response = requests.put("https://api.lifx.com/v1beta1/lights/all/state", headers=headers, params=params)
			# print response.text
			time.sleep(timeToNextStep)
			
	
	ppgplot.pgclos()
	
	
	sys.exit()

	