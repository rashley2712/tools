#!/usr/bin/env python

import argparse
from HTMLParser import HTMLParser
import urllib2
import sys, subprocess
import json
import datetime
import configHelper

if __name__ == "__main__":
	
	parser = argparse.ArgumentParser(description='Looks for the latest images from the SAFT webcam and makes a movie using "ffmpeg".')
	parser.add_argument('--default', action="store_true", help='Write the input parameters to the config file as default values.')
	args = parser.parse_args()
	
	
	sys.exit()
	
	"""Some ideas for video encoding... x=1; for i in *jpg; do counter=$(printf %03d $x); ln "$i" /tmp/img"$counter".jpg; x=$(($x+1)); done
	ffmpeg -f image2 -i /tmp/img%03d.jpg /tmp/a.mpg
	
	or
	
	ffmpeg -r 1 -pattern_type glob -i 'test_*.jpg' -c:v libx264 out.mp4
	ffmpeg -f image2 -framerate 10 -pattern_type glob -i '*.jpg' -r 10 a.avi
	
	"""
 
	
	