#!/usr/bin/env python

import argparse
import datetime
import numpy
import ppgplot
import generalUtils
from astropy.io import fits

if __name__ == "__main__":
	
	parser = argparse.ArgumentParser(description='Reads the images for a SAFT run. Plots and stacks them.')
	parser.add_argument('runfile', type=str, help='A text file containing the filenames of all of the images in the run. Ordered correctly.')
	parser.add_argument('--png', action='store_true', help='Switch to tell the program to output a .png file for each frame in the run.')
	args = parser.parse_args()
	
	imageIndex = 1
	
	filenames = []	
	filename = args.runfile
	fileList = open(filename, 'r')
	for line in fileList:
		filenames.append(str(line.strip()))
	fileList.close()
	
	numFrames = len(filenames)
	print "There are %d frames in this run."%numFrames
	
	
	frameFilename = filenames[10]
	
	hdulist = fits.open(frameFilename)
	
	print hdulist.info()
	for card in hdulist:
		# print card.header
		print card.header.keys()
		print repr(card.header)
	
	imageData =  hdulist[imageIndex].data
	hdulist.close()
	
	(height, width) = numpy.shape(imageData)
	
	""" Set up the PGPLOT windows """
	imagePlot = {}
	imagePlot['pgplotHandle'] = ppgplot.pgopen('/xs')
	ppgplot.pgpap(8, 1)
	ppgplot.pgenv(0., width,0., height, 1, -2)
	imagePlot['pgPlotTransform'] = [0, 1, 0, 0, 0, 1]
	
	
	boostedImage = generalUtils.percentiles(imageData, 20, 99)
	ppgplot.pggray(boostedImage, 0, width-1, 0, height-1, 0, 255, imagePlot['pgPlotTransform'])
	if args.png: generalUtils.writePNG(boostedImage, frameFilename)
	
	#txt = urwid.Text(u"Hello World")
	#fill = urwid.Filler(txt, 'top')
	#loop = urwid.MainLoop(fill)
	#loop.start()
	#loop.draw_screen()
	
	for index, frameFilename in enumerate(filenames):
		hdulist = fits.open(frameFilename)
		#txt = urwid.Text(u"Hello World")
		#fill = urwid.Filler(txt, 'top')
		#loop = urwid.MainLoop(fill)
		
		imageData =  hdulist[imageIndex].data
		boostedImage = generalUtils.percentiles(imageData, 20, 99)
		ppgplot.pggray(boostedImage, 0, width-1, 0, height-1, 0, 255, imagePlot['pgPlotTransform'])
		if args.png: generalUtils.writePNG(boostedImage, frameFilename)
		hdulist.close()
	
	#loop.stop()
	
	ppgplot.pgclos()
	
	
