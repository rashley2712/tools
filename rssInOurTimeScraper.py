#!/usr/bin/env python3
from html.parser import HTMLParser
from html.entities import name2codepoint
import argparse
import sys
import json
import os
import time
import random


class podcastMeta:
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

	def removeSummerRepeats(self):
		newList = []
		for meta in self.linkArray:
			title = meta['title']
			summer = False
			if "summer repeat".upper() in title.upper(): summer=True
			if summer:
				print(title, "is a summer repeat")
			else:
				newList.append(meta)
		self.linkArray = newList	

class MyHTMLParser(HTMLParser):
	def __init__(self, *args, **kwargs):
		super(MyHTMLParser, self).__init__(*args, **kwargs)
		self.divs = []
		self.programmes = []
		self.comments = []
		self.parseProgramme = False
		self.parseLink = False
		self.parseTitle = False
		self.parseSynopsis = False
		self.programme = {}
		self.programmeList = []

	def handle_starttag(self, tag, attrs):
		#print("Start tag:", tag)
		for attr in attrs:
			#print("     attr:", attr)
			if tag=="div":
				self.divs.append(attrs)
				if attr[0] == "class":
					if attr[1]=="programme__body":
						print("Found a programme!")
						self.programme = {}
						self.parseProgramme = True
			if attr[0] == "href" and tag=="a" and self.parseProgramme:
				print("link found...")
				print(attr[1])
				self.programme['link'] = attr[1]
			if attr[0] == "class" and tag=="span" and self.parseProgramme:
				if "programme__title" in attr[1]:
					self.parseTitle = True
			if attr[0] == "class" and tag=="p" and self.parseProgramme:
				if "programme__synopsis" in attr[1]:
					self.parseSynopsis = True

	def handle_endtag(self, tag):
		#print("End tag  :", tag)
		if tag=="div" and self.parseProgramme:
			self.parseProgramme = False
			print("stopped parsing programme")
			print(self.programme)
			self.programmeList.append(self.programme)
		if tag=="span" and self.parseSynopsis:
			self.parseSynopsis = False

	def handle_data(self, data):
		if self.parseProgramme:
			print("Data     :", data)
		if self.parseTitle:
			self.programme['title'] = data
			print("Title:", data)
			self.parseTitle = False
		if self.parseSynopsis:
			if hasattr(self.programme,'synopsis'): self.programme['synopsis']+= data
			else: self.programme['synopsis'] = data
			print("Synopsis:", data)
			#self.parseSynopsis = False
			
	def handle_comment(self, data):
		self.comments.append(data)
		#print("Comment  :", data)

	def handle_entityref(self, name):
		c = chr(name2codepoint[name])
		#print("Named ent:", c)

	def handle_charref(self, name):
		if name.startswith('x'):
			c = chr(int(name[1:], 16))
		else:
			c = chr(int(name))
		#print("Num ent  :", c)

	def handle_decl(self, data):
		pass
		#print("Decl     :", data)

	def getProgrammes(self):
		return self.programmeList

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Opens up a URL on the BBC site and looks for In Our Time download links')
	parser.add_argument('--url', type=str, help='URL to scrape. Default is: https://www.bbc.co.uk/programmes/b006qykl/episodes/player')
	parser.add_argument('--outdir', type=str, default = "/Users/rashley/Radio/InOurTime", help='Directory to write the downloaded files. Default is: /Users/rashley/Radio/InOurTime/')
	args = parser.parse_args()
	if args.url==None:
		baseURL = "https://www.bbc.co.uk/programmes/b006qykl/episodes/player"
		#fullURL = "http://localhost/test.html"
	else:
		baseURL = args.url
	

	timeBase = 5
	
	for page in range(1,100):
		print(page)

		fullURL = baseURL + "?page=%d"%page
		print("Ready to fetch: ", fullURL)
		
		parser = MyHTMLParser()
		HTMLTest = "<b>hello</b>"
		import urllib.request
		f = urllib.request.urlopen(fullURL)
		pageString = f.read().decode('utf-8')
		f.close()
		parser.feed(pageString)

		programmes = parser.getProgrammes()
		count = 0
		allPodcasts = podcastMeta()
		allPodcasts.load()
		for entry in programmes:
			podcast = { 'title': entry['title'], 'description': entry['synopsis'], 'link' : entry['link'], 'downloaded': False}
			print(entry['title'])
			allPodcasts.add(podcast)
			count=count+1
		print("Number of entries:", count)
		allPodcasts.removeSummerRepeats()
		allPodcasts.save()
		waitTime = timeBase + random.random()*4
		time.sleep(waitTime)