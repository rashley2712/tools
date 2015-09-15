#!/usr/bin/env python

import sys, subprocess, eyed3, os, re
import argparse
import inspect
import shutil

def isprop(v):
	return isinstance(v, property)

if __name__ == "__main__":
	
	parser = argparse.ArgumentParser(description='Converts a file to mp3 format and adds some ID3 tages.')
	parser.add_argument('filename', type=str, help='Filename to convert.')
	parser.add_argument('--copy', action='store_true', help="Copy file to the upload folder.")
	parser.add_argument('--skip', action='store_true', help='Skip the conversion step.')
	args = parser.parse_args()
	uploadFolder = "/Users/rashley/Radio/upload/"
	
	audioFilename = args.filename
	filenameParts = os.path.splitext(audioFilename)
	outputFilename = filenameParts[0]
	
	replacePattern = "_b......._default"
	runs_re = re.compile(replacePattern)
	m = runs_re.search(outputFilename)
	if m!=None:
		outputFilename = outputFilename[:-len(replacePattern)]
	outputFilename+= ".mp3"
	
	print "Converting %s to %s"%(audioFilename, outputFilename)
	
	if not args.skip:
		subprocess.call(["ffmpeg","-i", audioFilename, "-acodec", "libmp3lame", "-ar", "22050", "-ab", "64k", outputFilename])

	audioData = eyed3.load(outputFilename)
	
	members = inspect.getmembers(audioData.tag)
	# for m in members:
	#	print m
	
	print "Title:", audioData.tag.title
	print "Artist:", audioData.tag.artist
	print "Album:", audioData.tag.album
	
	newFilename = outputFilename.replace("_default", "")
	print "New filename:", newFilename
	
	if (args.copy):
		shutil.copy2(outputFilename, uploadFolder + outputFilename)
	
	sys.exit()
	
	
	