#!/usr/bin/env python

import argparse
from HTMLParser import HTMLParser
import urllib2
import sys, subprocess
import json
import datetime

def createMovie(path):
	if path==None: path = ""
	print "Creating the movie"
	movieFilename = "auto_test.mp4"
	subprocess.call(["mencoder", "mf://*.jpg", "-o", movieFilename, "-fps", "8", "-ovc", "lavc"])

if __name__ == "__main__":
	
	parser = argparse.ArgumentParser(description='Fetches the latest SAFT image and stores it locally.')
	parser.add_argument('--url', type=str, help='URL to find image. Default is: http://wasp.warwick.ac.uk/swasp/main/cam1/image.jpg')
	parser.add_argument('--prefix', type=str, help='Prefix for the filenames')
	parser.add_argument('--outputdir', type=str, help='Optional output directory (must exist already)')
	parser.add_argument('--createmovie', action='store_true', help='Create a movie from all of the saved image files. Surpresses fetching of the latest image.')
	args = parser.parse_args()
	
	if args.createmovie:
		createMovie(args.outputdir)
		sys.exit()
	
	if args.url==None:
		fullURL = "http://wasp.warwick.ac.uk/swasp/main/cam1/image.jpg"
	else:
		fullURL = args.url
	if args.prefix==None:
		prefix = ""
	else:
		prefix = args.prefix + "-"
	if args.outputdir!=None:
		prefix = args.outputdir + "/" + prefix
	
	print "Ready to fetch: ", fullURL
	
	try:
		response = urllib2.urlopen(fullURL)
	except  urllib2.HTTPError as e:
		print "We got an error of:", e.code
		sys.exit()
	except urllib2.URLError as e:
		print e.reason
		sys.exit()

	headers = str(response.headers)
	
	pageData = response.read()
	print "Fetched the data ok"
	
	now = datetime.datetime.now()
	
	outputFilename = "%s%s%s%s_%s%s.jpg"%(prefix, str(now.year), str(now.month).zfill(2), str(now.day).zfill(2), str(now.hour).zfill(2), str(now.minute).zfill(2))
	print "Writing to:", outputFilename
	outputFile = open(outputFilename, 'w')

	outputFile.write(pageData)
	outputFile.close()
	

	response.close()
	
	"""Some ideas for video encoding... x=1; for i in *jpg; do counter=$(printf %03d $x); ln "$i" /tmp/img"$counter".jpg; x=$(($x+1)); done
	ffmpeg -f image2 -i /tmp/img%03d.jpg /tmp/a.mpg
	
	or
	
	ffmpeg -r 1 -pattern_type glob -i 'test_*.jpg' -c:v libx264 out.mp4
	
	ffmpeg -f image2 -framerate 10 -pattern_type glob -i '*.jpg' -r 10 a.avi
	"""
 
	
	