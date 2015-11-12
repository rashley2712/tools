#!/usr/bin/env python

import argparse
from HTMLParser import HTMLParser
import urllib2
import sys, subprocess, os
import json, re
import datetime
import shutil
import configHelper

if __name__ == "__main__":
	
	parser = argparse.ArgumentParser(description='Looks for the latest images from the SAFT webcam and makes a movie using "ffmpeg".')
	parser.add_argument('--save', action="store_true", help='Write the input parameters to the config file as default values.')
	parser.add_argument('--archive', action="store_true", help="Archive the used jpg files to a tarball.")
	parser.add_argument('--publish', action="store_true", help="Publish the new videos to the web folder.")
	parser.add_argument('--web', type=str, help="Specify the location of the web publishing directory.")
	parser.add_argument('--image', type=str, help="Specify the location of the raw jpg images.")
	args = parser.parse_args()
	
	configObject = configHelper.configClass("saftmovie")
	
	if args.image!=None:
		configObject.imageDirectory = args.image
	imageDirectory = configObject.getProperty("imageDirectory")
	if imageDirectory == None:
		print "ERROR: Please specify the directory where the raw images are using the --image parameter"
		sys.exit()
	
	
	if args.web!=None:
		configObject.webDirectory = args.web
	webDirectory = configObject.getProperty("webDirectory")
	if webDirectory == None:
		print "ERROR: Please specify the directory of the web pages using the --web parameter"
		sys.exit()
		
	if args.save:
		configObject.save()

	today = datetime.date.today()

	todayString = str(today).replace("-","")
	
	try:
		fileList = os.listdir(imageDirectory)
	except:
		print "Could not find the directory %s. Exiting."%imageDirectory
		sys.exit(-1)
	
	date_re = re.compile(r'20[0-9]{2}([0-9]{2}){2}')
	
	uniqueDates = []
	jpgFileList = []
	for filename in fileList:
		if ".jpg" in filename: jpgFileList.append(filename)

	for filename in jpgFileList:
		d = date_re.search(filename)
		if (d):
			date = d.group(0)
			if date not in uniqueDates:
				uniqueDates.append(date)
			
	print "Unique dates:", uniqueDates
	
	filesByDate = []
	for uniqueDate in uniqueDates:
		filesForDate = {}
		filesForDate['date'] = uniqueDate
		files = []
		for filename in fileList:
			d = date_re.search(filename)
			if (d):
				date = d.group(0)
				if date == uniqueDate and ".jpg" in filename: files.append(filename)
		filesForDate['files'] = files
		filesByDate.append(filesForDate)
			
	for f in filesByDate:
		print "Date: %s  Number of files found: %d"%(f['date'], len(f['files']))
		files = sorted(f['files'], key=lambda object: object, reverse = False)
		f['files'] = files
		filelistName = "%s.list"%f['date']
		listFile = open(filelistName, 'wt')
		for n in f['files']:
			listFile.write(imageDirectory + "/" + n + '\n')
		listFile.close() 
		
	for f in filesByDate:
		print "Making movie for %s."%f['date'], imageDirectory
		ffmpegCommand = ["/home/rashley/code/tools/pipeFFMPEG.bash"]
		ffmpegCommand.append(f['date'])
		print "Running:", ffmpegCommand
		subprocess.call(ffmpegCommand)
		
	if args.archive:
		for f in filesByDate:
			print "Archiving files for %s."%(f['date']) 
			tarCommand = ['tar']
			tarCommand.append('-cf')
			tarCommand.append('%s.tar'%f['date'])
			tarCommand.append('-T')
			tarCommand.append('%s.list'%f['date'])
			print "Executing:", tarCommand
			subprocess.call(tarCommand)
			
			if todayString in f['date']:
				print "Not removing today's images: %s."%todayString
				continue


			for filename in f['files']:
				print "Removing:", filename
				os.remove(imageDirectory + "/" + filename)
				
		listFiles = os.listdir(".")
		for l in listFiles:
			if '.list' in l:
				os.remove(l)
				
		for l in listFiles:
			if '.tar' in l:
				fromName = l
				toName = imageDirectory + "/tar/" + l
				print fromName, " --> ", toName
				shutil.move(fromName, toName)
			
	if args.publish:
		print "Publishing:"
		allFiles = os.listdir(".")
		for f in allFiles:
			if ".mp4" in f: 
				fromName = f
				toName = webDirectory + "/" + f
				print fromName, " --> ", toName
				shutil.move(fromName, toName)
			
	sys.exit()
	
	"""Some ideas for video encoding... x=1; for i in *jpg; do counter=$(printf %03d $x); ln "$i" /tmp/img"$counter".jpg; x=$(($x+1)); done
	ffmpeg -f image2 -i /tmp/img%03d.jpg /tmp/a.mpg
	
	or
	
	ffmpeg -r 1 -pattern_type glob -i 'test_*.jpg' -c:v libx264 out.mp4
	ffmpeg -f image2 -framerate 10 -pattern_type glob -i '*.jpg' -r 10 a.avi
	
	"""
 
	
	
