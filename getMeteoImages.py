#!/usr/bin/env python3

import argparse, os
#from HTMLParser import HTMLParser
#from bs4 import BeautifulSoup
import urllib.error
import urllib.request
import sys
import json, datetime
from PIL import Image
		
if __name__ == "__main__":
	
	parser = argparse.ArgumentParser(description='Opens up a URL for the La Palma Meteo site and doanloads images.')
	parser.add_argument('--show', action='store_true', help='Show the images in a window on the desktop.')
	parser.add_argument('-o','--outputpath', type=str, default="", help='Specify and output directory for the images.')
	parser.add_argument('-w','--workingdir', type=str, default="/tmp/", help='Working directory for temporary files. Defaults to /tmp')
	
	args = parser.parse_args()
	
	baseURL = "http://lapalma.hdmeteo.com/"
	user = "meteo-mont-tricias"
	baseImage = "maskroad.png"
	tempMap = "temp-pic.php"
	tempOverlay = "temp-overlay.php?user=%s"%user
	print("Base URL is:", baseURL) 

	now = datetime.datetime.now()
	timeString = now.strftime("%Y%m%d_%H%M")
	print("Running the fetch at:",timeString)

	imagesToGet = [ {'url': baseURL + baseImage, 'output': args.workingdir + 'base.png' }, 
	                {'url': baseURL + tempOverlay, 'output': args.workingdir + 'temp-overlay_%s.png'%timeString },
					{'url': baseURL + tempMap, 'output': args.workingdir + 'temp-map_%s.png'%timeString } ]
	
	
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
	overlayImage.save(os.path.join(args.outputpath, "temp_%s.png"%timeString))
