#!/usr/bin/env python3

import argparse, os, subprocess
#from HTMLParser import HTMLParser
#from bs4 import BeautifulSoup
import urllib.error
import urllib.request
import sys
import json, datetime
from PIL import Image
		
if __name__ == "__main__":
	
	parser = argparse.ArgumentParser(description='Archives all of the meteo images and makes the animation.')
	parser.add_argument('-o','--outputpath', type=str, default="", help='This is the folder where the files are currently residing.')
	parser.add_argument('-w','--workingdir', type=str, default="/tmp/", help='Working directory for temporary files. Defaults to /tmp')
	parser.add_argument('-d','--date', type=str, default="yesterday", help='Date for the archive YYYYMMDD. Defaults to "yesterday".')
	
	args = parser.parse_args()
	
	baseURL = "http://lapalma.hdmeteo.com/"
	user = "meteo-mont-tricias"
	baseImage = "maskroad.png"
	tempMap = "temp-pic.php"
	tempOverlay = "temp-overlay.php?user=%s"%user
	print("Base URL is:", baseURL) 

	now = datetime.datetime.now()
	timeString = now.strftime("%Y%m%d_%H%M")
	if args.date == 'yesterday':
		yesterday = now - datetime.timedelta(days=1)
		yesterdayString = yesterday.strftime("%Y%m%d")
	else:
		yesterdayString = args.date
	print("Yesterday was:", yesterdayString)

	archiveFolder = os.path.join(args.outputpath, yesterdayString)
	print("Archiving to: %s"%archiveFolder)
	if not os.path.exists(archiveFolder):
		os.mkdir(archiveFolder)
	
	# Collect all the files belonging to that date in the outputfolder
	files = os.listdir(args.outputpath)
	fileCollection = []
	for f in files:
		if "temp_%s"%yesterdayString in f:
			fileCollection.append(f)

	fileCollection = sorted(fileCollection)
	
	for f in fileCollection:
		originalPath = os.path.join(args.outputpath, f)
		destinationPath = os.path.join(archiveFolder, f)
		print("Renaming %s to %s"%(originalPath, destinationPath))
		os.rename(originalPath, destinationPath)

	# Regenerate the file list now in the archive folder
	fileCollection = []
	files = os.listdir(archiveFolder)
	for f in files:
		if "temp_%s"%yesterdayString in f:
			fileCollection.append(f)

	fileCollection = sorted(fileCollection)
	listFile = open(os.path.join(archiveFolder, "%s.list"%yesterdayString), 'wt')
	for f in fileCollection:
		listFile.write("%s\n"%f)
	listFile.close()

	user = os.getlogin()
	ffmpegCommand = ["/home/%s/bin/pipeFFMPEG.bash"%user]
	ffmpegCommand.append(yesterdayString)
	print("Running:", ffmpegCommand)
	from subprocess import Popen, PIPE
	#output, errors = Popen(archiveFolder, stdout=PIPE, stderr=PIPE).communicate()
	os.chdir(archiveFolder)
	subprocess.call(ffmpegCommand)
	os.rename(os.path.join(archiveFolder, yesterdayString+".mp4"), os.path.join(args.outputpath, yesterdayString + ".mp4"))

	sys.exit()

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
