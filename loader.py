#!/usr/bin/env python

import argparse
import Image,ImageDraw,ImageFont
import matplotlib.pyplot
import matplotlib.image
import numpy

if __name__ == "__main__":
	

	parser = argparse.ArgumentParser(description='Loads the jpeg file and gives us some information about it...')
	parser.add_argument('filename', type=str, help='The name of an image file')

	args = parser.parse_args()
	
	print args
	
	imageData=matplotlib.image.imread(args.filename)
	
	print imageData.shape
	
	imgplot = matplotlib.pyplot.imshow(imageData)
	
	matplotlib.pyplot.show()
	