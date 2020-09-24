#!/usr/bin/env python

import argparse
from HTMLParser import HTMLParser
from bs4 import BeautifulSoup
import urllib
import sys
import json


# create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):
	parseData = False
	gettingRecord = False
	fieldName = None
	dataRecord = None
	
	def handle_starttag(self, tag, attrs):
		if "span" in tag:
			print "span tag"
			# print attrs
			for attribute in attrs:
				print attribute
				if "name" in attribute[1]:
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
	parser.add_argument('--outdir', type=str, default = "/Users/rashley/Radio/InOurTime", help='Directory to write the downloaded files. Default is: /Users/rashley/Radio/InOurTime/')
	
	args = parser.parse_args()
	if args.url==None:
		fullURL = "http://www.bbc.co.uk/programmes/b006qykl/episodes/downloads"
		fullURL = "http://localhost/bbc_test.html"
		fullURL = "http://www.bbc.co.uk/programmes/b006qykl/episodes/downloads.rss"
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
	
	mp3Links = []
	#HTMLparser = MyHTMLParser()
	#HTMLparser.feed(pageData)
	
	soup = BeautifulSoup(pageData, 'html.parser')
	
	titles = []
	for title in soup.find_all('title'):
		titles.append(title.get_text())
	
	links = []
	for link in soup.find_all('link'):
	    links.append(link.get_text())
		
	mp3Objects = []
	for t, l in zip(titles, links):
		mp3 = {}
		mp3['title'] = t
		mp3['url'] = l
		filename = t.strip()
		filename = filename.replace(' ', '_')
		filename = filename.replace('\'', '')
		filename = "IOT_%s.mp3"%filename
		mp3['filename'] = filename
		mp3Objects.append(mp3)
		
	filteredList = []
	for m in mp3Objects:
		print m
		if ".mp3" in m['url']:
			filteredList.append(m)
	mp3Objects = filteredList
	
	response.close()
	
	for mp3 in mp3Objects:
	
		print "Ready to get:", mp3
		try:
			response = urllib2.urlopen(mp3['url'])
			outputFilename = "%s/%s"%(args.outdir, mp3['filename'])
			outfile = open(outputFilename, 'w')
			outfile.write(response.read())
		except  urllib2.HTTPError as e:
			print "We got an error of:", e.code
		except urllib2.URLError as e:
			print e.reason
		
	
	sys.exit()
	
	 
	
	