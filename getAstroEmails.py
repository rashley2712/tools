#!/usr/bin/env python

import argparse
import datetime
import datetime
import sys
import urllib2
import os
from HTMLParser import HTMLParser

allURLs = []

# create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        # print "Encountered a start tag:", tag
        for attribute in attrs:
			if "href" in attribute[0]:
				allURLs.append(attribute[1])
    # def handle_endtag(self, tag):
        # print "Encountered an end tag :", tag
        
    # def handle_data(self, data):
        # print "Encountered some data  :", data
      

def filterListByString(items, match):
	newList = []
	for i in items:
		if match in i:
			newList.append(i)
	return newList			  
        

if __name__ == "__main__":
	
	testBaseURL = "http://www.rashley.co.uk/maillist.html"
	
	baseURL = "http://fedastro.org.uk/fas/members/members-a-z/"
	homeDIR = os.getenv("HOME")
	dropboxPath = homeDIR + "/Dropbox/Crosswords/"
	namePrefix = "gdn.quick."
	nameSuffix = ".pdf"

	parser = argparse.ArgumentParser(description='Downloads email list and puts it into a Google doc.')
	parser.add_argument('--test', action='store_true', help='Use the test URL instead of the real URL.')
	
	arg = parser.parse_args()
	print arg
	if arg.test:
		baseURL = testBaseURL
		
	
	fullURL = baseURL
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
	parser = MyHTMLParser()
	parser.feed(pageData)

	response.close()
		
	allURLs = filterListByString(allURLs, 'cms-society2')

	for i, u in enumerate(allURLs):
		print i, u
	
	
	entries = []
	
	for URL in allURLs:
		
		entry = {}
		
		print "Now going to fetch:", URL
	
		try:
			response = urllib2.urlopen(URL)
		except  urllib2.HTTPError as e:
			print "We got an error of:", e.code
			sys.exit()
		except urllib2.URLError as e:
			print e.reason
			sys.exit()
	
		headers = str(response.headers)
		
		pageData = response.read()
		print pageData
		
		startName = pageData.find("Society Info:")
		startName+= +  len("Society Info:") + 1
		endName = pageData.find("<", startName)
		name = pageData[startName:endName]
		print "Their name:", name
		entry['name'] = name
		
		startWebpage = pageData.find("href")
		startWebpage+= +  len("href=") + 1
		endWebpage = pageData.find("'", startWebpage)
		link = pageData[startWebpage:endWebpage]
		print "Their website:", link
		entry['link'] = link
		
		startEmail = pageData.find("mailto:")
		startEmail+= +  len("mailto:") 
		endEmail = pageData.find("'", startEmail)
		
		email = pageData[startEmail:endEmail]
		print "Their email:", email
		entry['email'] = email
		
		response.close()
	
		entries.append(entry)
		
	# Create the CSV file
	filename = "astroemails.csv"
	outfile = open(filename, 'wt')
	outfile.write("Name, Website, Email\n")
	for e in entries:
		outfile.write("%s, %s, %s\n"%(e['name'], e['link'], e['email']))

	outfile.close()
