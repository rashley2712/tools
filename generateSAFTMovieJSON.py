#!/usr/bin/env python 

import argparse
import sys, subprocess, os
import json, re
import datetime
import configHelper

if __name__ == "__main__":
	
	parser = argparse.ArgumentParser(description='Looks into the web directory of the SAFT movies and creates an updated JSON file for the web client to read.')
	parser.add_argument('--default', action="store_true", help='Write the input parameters to the config file as default values.')
	parser.add_argument('--archive', action="store_true", help="Archive the used jpg files to a tarball.")
	parser.add_argument('--publish', action="store_true", help="Publish the new videos to the web directory.")
	args = parser.parse_args()
	
	webDirectory = "/data/rashley/www/saftvideo"
	
	configObject = configHelper.configClass("saftmovie")
	configObject.getProperty("webDirectory")
	configObject.setProperty("webDirectory", "/data/rashley/www/saftvideo")
	configObject.save()
	
	today = datetime.date.today()

	todayString = str(today).replace("-","")
	
	try:
		fileList = os.listdir(webDirectory)
	except:
		print "Could not find the directory %s. Exiting."%webDirectory
		sys.exit(-1)
	
	date_re = re.compile(r'20[0-9]{2}([0-9]{2}){2}')
	
	movies = []
	mp4FileList = []
	for filename in fileList:
		if ".mp4" in filename: mp4FileList.append(filename)

	for filename in mp4FileList:
		d = date_re.search(filename)
		if (d):
			date = d.group(0)
			movieFile = {}
			movieFile['filename'] = filename
			movieFile['date'] = date
			movies.append(movieFile)
			
	print "Movies:", movies
	
	JSONfilename = webDirectory + "/movies.json"
	
	JSONfile = open(JSONfilename, 'w')
	
	JSONfile.write(json.dumps(movies))
	
	JSONfile.close()
	
	
