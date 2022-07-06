#!/usr/bin/env python3
from html.parser import HTMLParser
from html.entities import name2codepoint
import urllib.request
import argparse
import sys
import json
import os
import time
import random
import requests

class podcastMeta:
	def __init__(self):
		self.linkArray = []
		self.filename = "links.json"

	def load(self):
		if not os.path.exists(self.filename): return
		inputFile = open(self.filename, 'rt')
		self.linkArray = json.load(inputFile)
		inputFile.close()

	def setDownloaded(self, link):
		for l in self.linkArray:
			if l['link'] == link: 
				l['downloaded'] = True
				return


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
		self.links = []

	def handle_starttag(self, tag, attrs):
		if tag=="a": 
			for attr in attrs:
				if attr[0]=="href": self.links.append(attr[1])
	
		for attr in attrs:
			if tag=="div":
				self.divs.append(attrs)
				if attr[0] == "class":
					if attr[1]=="programme__body":
						#print("Found a programme!")
						self.programme = {}
						self.parseProgramme = True
			if attr[0] == "href" and tag=="a" and self.parseProgramme:
				#print("link found...")
				#print(attr[1])
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
			#print("stopped parsing programme")
			#print(self.programme)
			self.programmeList.append(self.programme)
		if tag=="span" and self.parseSynopsis:
			self.parseSynopsis = False

	def handle_data(self, data):
		if self.parseProgramme:
			#print("Data     :", data)
			pass
		if self.parseTitle:
			self.programme['title'] = data
			#print("Title:", data)
			self.parseTitle = False
		if self.parseSynopsis:
			if hasattr(self.programme,'synopsis'): self.programme['synopsis']+= data
			else: self.programme['synopsis'] = data
			#print("Synopsis:", data)
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
	parser = argparse.ArgumentParser(description='Opens up the links.json db and downloads the podcasts')
	parser.add_argument('--db', type=str, help='database of links. Default is: links.json')
	parser.add_argument('--outdir', type=str, default = "/home/rashley/Radio/InOurTime", help='Directory to write the downloaded files. Default is: /Users/rashley/Radio/InOurTime/')
	args = parser.parse_args()
	
	timeBase = 1
	
	podcastDB = podcastMeta()
	podcastDB.load()

	downloaded = 0
	for p in podcastDB.linkArray:
		print(p)
		if p['downloaded']: downloaded+=1
	print("Total %d podcasts"%len(podcastDB.linkArray))
	print("%d downloaded already"%downloaded)
	print()

	limit = 1000
	for index, p in enumerate(podcastDB.linkArray):
		if index==limit: sys.exit()
		print("Getting %s"%p['title'])
		print(".... at %s"%p['link'])
		if p['downloaded']: 
			print("This is already downloaded...skipping")
			continue
		parser = MyHTMLParser()
		f = urllib.request.urlopen(p['link'])
		pageString = f.read().decode('utf-8')
		f.close()
		parser.feed(pageString)

		downloadLinks = []
		for link in parser.links:
			if "mp3" in link: downloadLinks.append(link)
		print("%d mp3 links found."%len(downloadLinks))
		if len(downloadLinks)==0:
			print("No downloads found... skipping...")
			continue

		time.sleep(timeBase + random.random()*4)
		print("Fetching:", downloadLinks[0])
		params = {}
		response = requests.get("https:" + downloadLinks[0], params=params)
		
		local_filename = os.path.join(args.outdir, p['title'].replace('/', '_'))
		local_filename = local_filename.replace(' ', '_')
		local_filename+=".mp3"

		totalbits = 0
		if response.status_code == 200:
			with open(local_filename, 'wb') as f:
				chunkSize = 1024000
				for chunk in response.iter_content(chunk_size = chunkSize):
					if chunk:
						totalbits += chunkSize
						#print("Downloaded",totalbits*1025,"KB...")
						f.write(chunk)
			print("written to", local_filename)
			podcastDB.setDownloaded(p['link'])
			podcastDB.save()
		response.close()

		print()

	sys.exit()
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