#!/usr/bin/env python

import argparse
from HTMLParser import HTMLParser
import urllib2
import sys, os

outputFile = None

# create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):
	
        
	def handle_data(self, data):
		print "data:", data
		outputFile.write(data)
		outputFile.write(' ')
		
				
if __name__ == "__main__":
	
	parser = argparse.ArgumentParser(description='Opens up a file (or URL), strips out all of the HTML and returns as a text based list. ')
	parser.add_argument('filename', type=str, help='The filename to strip.')
	parser.add_argument('-o', '--output', type=str, help='The output filename. If left out, the .html extension will be replaced with a .txt extension.')
	parser.add_argument('-u', '--url', action='store_true', help='The filename is a URL. The page at this location will be fetched and stripped.')
	
	args = parser.parse_args()
	
	
	if args.url:
		try:
			fullURL = args.filename
			response = urllib2.urlopen(fullURL)
		except  urllib2.HTTPError as e:
			print "We got an error of:", e.code
			sys.exit()
		except urllib2.URLError as e:
			print e.reason
			sys.exit()
		except ValueError as e:
			print "%s does not seem to be a URL. Exiting."%args.filename
			sys.exit()
			

		headers = str(response.headers)
	
		pageData = response.read()
	
	try:
		inputFile = open(args.filename, 'r')
		pageData = inputFile.read()
	except Exception as e:
		print "Could not open the file: %s"%args.filename
	
	filenameParts = os.path.splitext(args.filename)
	
	if args.output==None:
		if filenameParts[1] == '.txt':
			print "Filename already has a '.txt' extension. Exiting."
			sys.exit()
		else:
			outputFilename = filenameParts[0] + ".txt"
	else:
		outputFilename = args.output
		if outputFilename == args.filename:
			print "Output filename is the same as input filename. Exiting."
			sys.exit()
	
	print "Converting %s to %s"%(args.filename, outputFilename)

	outputFile = open(outputFilename, 'w')
	HTMLparser = MyHTMLParser()
	HTMLparser.feed(pageData)

	if args.url: response.close()
	else: inputFile.close()
	outputFile.close()
	
	sys.exit()
	
	
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
	
	HTMLparser = MyHTMLParser()
	HTMLparser.feed(pageData)
	
	for g in gaiaAlerts:
		print g
	print "Found %d Gaia alert records."%len(gaiaAlerts)

	response.close()
	
	jsonFile = open("gaiaAlerts.json", "w")
	json.dump(gaiaAlerts, jsonFile)
	jsonFile.close()
	 
	
	
