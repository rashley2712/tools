#!/usr/bin/env python

import argparse
from PIL import Image 
import matplotlib.pyplot
import matplotlib.image
import numpy
import os

if __name__ == "__main__":
	

	parser = argparse.ArgumentParser(description='Loads the jpeg file and crops it...')
	parser.add_argument('filename', type=str, help='The name of an image file')

	args = parser.parse_args()
	
	print args
	
	inputFilename = args.filename
	filenameParts = os.path.splitext(inputFilename)
	outputFilename = filenameParts[0] + '_cropped' + filenameParts[1]
	print outputFilename
	
	
	print "Python Image Library version:", Image.VERSION
	
	image = Image.open(args.filename)
	
	print image.bits, image.size, image.format, image.mode
	
	redData, greenData, blueData = image.split()
	
	print numpy.shape(redData)
	
	box = (2000, 1000, 3500, 2500)
	croppedImage = image.crop(box)
	
	croppedImage.save(outputFilename)
	image.close()
	
	