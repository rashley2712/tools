#!/usr/bin/env python

import argparse
import datetime
import sys
import urllib2
import os
import json
from BeautifulSoup import BeautifulSoup

class allLinks:
	def __init__(self):
		self.linkArray = []
		self.filename = "links.json"


	def load(self):
		if not os.path.exists(self.filename): return
		inputFile = open(self.filename, 'rt')
		self.linkArray = json.load(inputFile)
		inputFile.close()

	def save(self):
		outFile = open(self.filename, 'wt')
		json.dump(self.linkArray, outFile, indent=4)
		outFile.close()

	def duplicate(self, link):
		for l in self.linkArray:
			if l['title'] == link['title']: return True
			if l['link'] == link['link']: return True

	def add(self, link):
		if not self.duplicate(link):
			self.linkArray.append(link)
		else:
			print("Duplicate detected: %s - %s"%(link['title'], link['link']))



if __name__ == "__main__":
	# http://open.live.bbc.co.uk/mediaselector/6/redir/version/2.0/mediaset/audio-nondrm-download-low/proto/http/vpid/p06c9hhm.mp3
	# http://open.live.bbc.co.uk/mediaselector/6/redir/version/2.0/mediaset/audio-nondrm-download/proto/http/vpid/p06c9hhm.mp3
	# http://open.live.bbc.co.uk/mediaselector/6/redir/version/2.0/mediaset/audio-nondrm-download/proto/http/vpid/p003k9c1.mp3
	# http://open.live.bbc.co.uk/mediaselector/6/redir/version/2.0/mediaset/audio-nondrm-download/proto/http/vpid/p05jqtcs.mp3
	# http://open.live.bbc.co.uk/mediaselector/6/redir/version/2.0/mediaset/audio-nondrm-download/proto/http/vpid/p04m6y80.mp3
	# http://open.live.bbc.co.uk/mediaselector/6/redir/version/2.0/mediaset/audio-nondrm-download/proto/http/vpid/p02q5c8r.mp3
	baseURL = "https://www.bbc.co.uk/programmes/b006qykl/episodes/a-z/"
	homeDIR = os.getenv("HOME")
	fetch = True
	
	parser = argparse.ArgumentParser(description='Downloads all of the In Our Time audio programmes.')
	parser.add_argument('-g', action='store_true', help='\'Get\' directive. Asks the script to get the crossword.')
	
	arg = parser.parse_args()
	print arg
	
	linkDB = allLinks()
	linkDB.load()
	
	if not arg.g:
		print "You did not specify the 'get' directive, so not really fetching the programmes."
		fetch=False

	letters = 'abcdefghijklmnopqrstuvwxyz'
	# letters = 'bcdefghijkl'
	
	for index in range(len(letters)):
		fullURL = baseURL + letters[index]
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
		print(headers)

		content = response.read()
		soup = BeautifulSoup(content)

		links = soup.findAll('a')
		print("%d links found."%len(links))
		for l in links:
			aclass = l.get('class')
			if aclass == 'box-link__target link--block ':
				link = l['href']
				#print("link: " + link)
				snippet = str(l)
				first = snippet[snippet.find("gel-pica-bold")+15:]
				substring = first[:first.find("span")-2]
				#print(snippet)
				print(substring, link)
				linkObject = {'title': substring, 'link': link}
				linkDB.add(linkObject)

		response.close()

		linkDB.save()
	print 'Completed successfully'