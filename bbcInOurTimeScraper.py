#!/usr/bin/env python

import argparse
from HTMLParser import HTMLParser
import urllib2
import sys
import json


# create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):
	parseData = False
	gettingRecord = False
	fieldName = None
	dataRecord = None
	
	def handle_starttag(self, tag, attrs):
		if "td" in tag:
			# print "Table data tag"
			# print attrs
			for attribute in attrs:
				if "views-field-field" in attribute[1]:
					classes = attribute[1].split(' ')
					for c in classes:
						if "views-field-field" in c:
							fieldName = c
					fieldName = fieldName[len("views-field-field-"):]
					print "Found alert data [%s]"%fieldName
					self.parseData = True
					self.fieldName = fieldName
				if "views-field-field-alert-name" in attribute[1]:
					self.gettingRecord = True
					self.dataRecord = {}
		
	def handle_endtag(self, tag):
		if "td" in tag: 
			# print "Found end <td> tag"
			self.parseData = False
		if "span" in tag:
			self.parseData = False
		if "tr" in tag and self.gettingRecord: 
			# print "Found end <tr> tag"
			self.gettingRecord = False
			gaiaAlerts.append(self.dataRecord)
			# print "Added.... Data record", self.dataRecord
		
        
	def handle_data(self, data):
		if self.parseData:
			if self.gettingRecord:
				data = data.strip()
				print "%s data: %s"%(self.fieldName, data)
				self.dataRecord[self.fieldName] = data
				
if __name__ == "__main__":
	
	parser = argparse.ArgumentParser(description='Opens up a URL on the BBC site and looks for In Our Time download links')
	parser.add_argument('--url', type=str, help='URL to scrape. Default is: http://www.bbc.co.uk/programmes/b006qykl/episodes/downloads')
	
	args = parser.parse_args()
	if args.url==None:
		fullURL = "http://www.bbc.co.uk/programmes/b006qykl/episodes/downloads"
		fullURL = "http://localhost/bbc_test.html"
	else:
		fullURL = args.url
	
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
	
	gaiaAlerts = []
	HTMLparser = MyHTMLParser()
	HTMLparser.feed(pageData)
	
	for g in gaiaAlerts:
		print g
	print "Found %d Gaia alert records."%len(gaiaAlerts)

	response.close()
	
	jsonFile = open("gaiaAlerts.json", "w")
	json.dump(gaiaAlerts, jsonFile)
	jsonFile.close()
	 
	
	