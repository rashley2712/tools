#!/usr/bin/env python

import sys, subprocess,  os, re
import argparse
import inspect
import shutil

def isprop(v):
	return isinstance(v, property)

if __name__ == "__main__":
	
	parser = argparse.ArgumentParser(description='Converts a file to mp3 format and adds some ID3 tages.')
	parser.add_argument('filename', type=str, help='Filename to convert.')
	parser.add_argument('--list', action="store_true", help='Filename is a list of files.')
	parser.add_argument('--copy', action='store_true', help="Copy file to the upload folder.")
	parser.add_argument('--skip', action='store_true', help='Skip the conversion step.')
	args = parser.parse_args()
	uploadFolder = "/home/rashley/Radio/converted/"
	
	files = []
	if args.list:
		fileInput = open(args.filename, 'rt')
		for line in fileInput:
			if len(line)<3: continue
			files.append(line.strip())
	else:
		files = [ args.filename ]

	for audioFilename in files:
		filenameParts = os.path.splitext(audioFilename)
		outputFilename = os.path.join(uploadFolder, audioFilename)
		if os.path.exists(outputFilename):
			print("File already exists...skipping.")
			continue
		print("Converting %s to %s"%(audioFilename, outputFilename))
		
		if not args.skip:
			subprocess.call(["ffmpeg","-i", audioFilename, "-acodec", "libmp3lame", "-ar", "22050", "-ab", "64k", outputFilename])
		
	sys.exit()
	
	
	