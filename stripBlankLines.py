#!/usr/bin/env python3

import argparse, os
import sys

if __name__ == "__main__":
	
	parser = argparse.ArgumentParser(description='Reads a text file and echos it to stdout removing any blank lines.')
	parser.add_argument('file', type=str, help='Filename.')
	args = parser.parse_args()
	
	filename = args.file
	readFile = open(filename, 'rt')
	for line in readFile:
		line = line.strip()
		if len(line)<1: continue
		print(line)
	readFile.close()
