#!/usr/bin/env python3

import argparse, os
#from HTMLParser import HTMLParser
#from bs4 import BeautifulSoup
import urllib.error
import urllib.request
import sys
import json, datetime
import HTMLdb

from PIL import Image
		
if __name__ == "__main__":
	
	parser = argparse.ArgumentParser(description='Opens up a URL for the La Palma Meteo site and doanloads images.')
	parser.add_argument('--show', action='store_true', help='Show the images in a window on the desktop.')
	parser.add_argument('-c','--config', type=str, default="autometeo.cfg", help='The config file.')
	args = parser.parse_args()
	
	configFile = open(args.config, 'rt')
	config = json.loads(configFile.read())
	print(config)

	db = HTMLdb.HTMLdb()
	db.filename = config['dbFile']
	db.load()
	db.dump()

	tempOverlay = "temp-overlay.php?user=%s"%config['user']
	humidityOverlay = "hum-overlay.php?user=%s"%config['user']
	cloudOverlay = "cloud-overlay.php?user=%s"%config['user']

	print("Base URL is:", config['baseURL']) 

	now = datetime.datetime.now()
	timeString = now.strftime("%Y%m%d_%H%M")
	print("Running the fetch at:",timeString)

	imagesToGet = [ {'url': config['baseURL'] + config['baseImage'], 'output': os.path.join(config['tmpPath'], 'base.png') }, 
	                {'url': config['baseURL'] + tempOverlay, 'output': os.path.join(config['tmpPath'],'temp-overlay_%s.png'%timeString) },
					{'url': config['baseURL'] + config['tempMap'], 'output': os.path.join(config['tmpPath'], 'temp-map_%s.png'%timeString) }, 
					{'url': config['baseURL'] + config['humidityMap'], 'output': os.path.join(config['tmpPath'], 'humidity-map_%s.png'%timeString) },
					{'url': config['baseURL'] + humidityOverlay, 'output': os.path.join(config['tmpPath'], 'humidity-overlay_%s.png'%timeString) },
					{'url': config['baseURL'] + config['cloudMap'], 'output': os.path.join(config['tmpPath'], 'cloud-map_%s.png'%timeString) },
					{'url': config['baseURL'] + cloudOverlay, 'output': os.path.join(config['tmpPath'], 'cloud-overlay_%s.png'%timeString) }
					 ]
	
	
	print(imagesToGet)

	for image in imagesToGet:
		if os.path.exists(image['output']): 
			print("skipping...%s"%image['url'])
			continue
		try:
			response = urllib.request.urlopen(image['url'])
		except  urllib.error.HTTPError as e:
			print("We got an error of:", e.code)
			sys.exit()
		except urllib.error.URLError as e:
			print(e.reason)
			sys.exit()

		headers = str(response.headers)
		print(headers)
		
		outFile = open(image['output'], 'wb')
		outFile.write(response.read())
		outFile.close()
	print("Fetched the data ok")

	image = imagesToGet[0]
	baseImage = Image.open(image['output'])
	if args.show: baseImage.show()
	print(baseImage.size, baseImage.info)
	temperatureOverlay = Image.open(imagesToGet[1]['output'])
	if args.show: temperatureOverlay.show()
	print(temperatureOverlay.size, temperatureOverlay.info)
	temperatureImage = Image.open(imagesToGet[2]['output'])
	if args.show: temperatureImage.show()
	print(temperatureImage.size, temperatureImage.info)
	overlayImage = Image.alpha_composite(temperatureImage, temperatureOverlay)
	if args.show: overlayImage.show(title="overlay")

	dateString = timeString[:-5]
	destinationFolder = os.path.join(config['HTMLPath'], dateString)
	if not os.path.exists(destinationFolder):
		os.mkdir(destinationFolder)
	destinationImage = os.path.join(destinationFolder,  "temp_%s.png"%timeString)
	
	overlayImage.save(destinationImage)
	webPathToImage = os.path.join(config['webRoot'], dateString,  "temp_%s.png"%timeString )
	db.set("latestTemperatureImage", webPathToImage)
	
	# Write the humidity image with its overlay
	humidityImage = Image.open(imagesToGet[3]['output'])
	if args.show: humidityImage.show()
	humidityOverlay = Image.open(imagesToGet[4]['output'])
	if args.show: humidityOverlay.show()
	overlayImage = Image.alpha_composite(humidityImage, humidityOverlay)
	if args.show: overlayImage.show()
	destinationImage = os.path.join(destinationFolder,  "humidity_%s.png"%timeString)
	overlayImage.save(destinationImage)
	webPathToImage = os.path.join(config['webRoot'], dateString,  "humidity_%s.png"%timeString )
	db.set("latestHumidityImage", webPathToImage)
	
	# Write the cloud image with its overlay
	cloudImage = Image.open(imagesToGet[5]['output'])
	if args.show: humidityImage.show()
	cloudOverlay = Image.open(imagesToGet[6]['output'])
	if args.show: humidityOverlay.show()
	overlayImage = Image.alpha_composite(cloudImage, cloudOverlay)
	if args.show: overlayImage.show()
	destinationImage = os.path.join(destinationFolder,  "cloud_%s.png"%timeString)
	overlayImage.save(destinationImage)
	webPathToImage = os.path.join(config['webRoot'], dateString,  "cloud_%s.png"%timeString )
	db.set("latestCloudImage", webPathToImage)
	
	db.set("lastUpdate", timeString)
	