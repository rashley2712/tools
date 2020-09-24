#!/usr/bin/env python3

import argparse
import datetime
import sys
import urllib
import os
import json
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
	
	def updateStatus(self, index):
		self.linkArray[index]['downloaded'] = True
		self.save()

	def size(self):
		return len(self.linkArray)

if __name__ == "__main__":
	homeDIR = os.getenv("HOME")
	fetch = True
	
	parser = argparse.ArgumentParser(description='Downloads all of the In Our Time audio programmes.')
	parser.add_argument('-l', '--list', action='store_true', help='Just list the podcasts.')
	
	args = parser.parse_args()
	
	linkDB = podcastMeta()
	linkDB.load()
	
	
	if args.list:
		for l in linkDB.linkArray:
			print(l['title'], l['downloaded'])


	#for index in range(len(linkDB.linkArray)):
	for index in range(linkDB.size()):	
		if linkDB.linkArray[index]['downloaded']: continue
		params = {}
		url = linkDB.linkArray[index]['link']
		print(index, " fetching ", linkDB.linkArray[index]['title'], " at ", url)
		response = requests.get(url, params=params)
		downloaded_file = response.content

		local_filename = linkDB.linkArray[index]['title']
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
			f.close()
			linkDB.updateStatus(index)