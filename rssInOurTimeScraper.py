#!/usr/bin/env python3
import feedparser
import argparse
import sys
import json

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
			
if __name__ == "__main__":
	
	parser = argparse.ArgumentParser(description='Opens up a URL on the BBC site and looks for In Our Time download links')
	parser.add_argument('--url', type=str, help='URL to scrape. Default is: https://podcasts.files.bbci.co.uk/b006qykl.rss')
	parser.add_argument('--outdir', type=str, default = "/Users/rashley/Radio/InOurTime", help='Directory to write the downloaded files. Default is: /Users/rashley/Radio/InOurTime/')
	
	args = parser.parse_args()
	if args.url==None:
		fullURL = "https://podcasts.files.bbci.co.uk/b006qykl.rss"
		#fullURL = "http://localhost/test.rss"
	else:
		fullURL = args.url
	
	print("Ready to fetch: ", fullURL)
	
	feed = feedparser.parse(fullURL)

	feed_title = feed['feed']['title']
	feed_entries = feed.entries

	count = 0
	allPodcasts = podcastMeta()
	for entry in feed.entries:
		podcast = { 'title': entry.title, 'description': entry.description, 'link' : entry.links[0].href, 'downloaded': False}
		print(entry.title)
		allPodcasts.add(podcast)
		count=count+1
	print("Feed title:", feed_title)
	print("Number of entries:", count)
	allPodcasts.save()
	allPodcasts.removeSummerRepeats()
	allPodcasts.save()
	