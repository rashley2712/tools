#!/usr/bin/env python

import argparse, sys
import datetime, time
import numpy
import ppgplot
import generalUtils, configHelper
import curses
from astropy.io import fits

if __name__ == "__main__":
	
	parser = argparse.ArgumentParser(description='Simulates a real run on the SAFT telescope.')
	parser.add_argument('runfile', type=str, help='A text file containing the filenames of all of the images that will be output from the \'run\'.')
	parser.add_argument('-o', '--outputDir', type=str, help='Folder to use for the output of the \'run\'.')
	parser.add_argument('--save', action="store_true", help='Write the input parameters to the config file as default values.')
	parser.add_argument('-e', '--exposureTime', type=float, help='Exposure time for the simulated exposures.')
	parser.add_argument('-r', '--readoutTime', type=float, help='Readout time for the simulated exposures.')
	args = parser.parse_args()
	print args
	
	config = configHelper.configClass("simulateSAFTRun")

	exposureTime = config.getProperty("ExposureTime")
	if args.exposureTime!=None:
		exposureTime = args.exposureTime
		config.ExposureTime = exposureTime
	if exposureTime == None:
		print "Please specify an exposure time or save one in the config file."
		sys.exit()
	
	readoutTime = config.getProperty("ReadoutTime")
	if args.readoutTime!=None:
		readoutTime = args.readoutTime
		config.ReadoutTime = readoutTime
	if readoutTime == None:
		print "Please specify a readout time or save one in the config file."
		sys.exit()

	outputDir = config.getProperty("OutputDirectory")
	if args.outputDir!=None:
		outputDir = args.outputDir
		config.OutputDirectory = outputDir
	if outputDir == None:
		outputDir = "."
		sys.exit()

	if args.save:
		config.save()
	
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
	
	imageData =  hdulist[0].data
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
	
	screen = curses.initscr()
	curses.noecho() 
	curses.curs_set(0) 
	screen.keypad(1)
	screen.addstr("This is a String")
	screen.addstr("This is a Sample Curses Script\n\n") 
	
	while True: 
	   event = screen.getch() 
	   if event == ord("q"): break 
	   elif event == ord("p"): 
	      screen.clear() 
	      screen.addstr("The User Pressed Lower Case p") 
	   elif event == ord("P"): 
	      screen.clear() 
	      screen.addstr("The User Pressed Upper Case P") 
	   elif event == ord("3"): 
	      screen.clear() 
	      screen.addstr("The User Pressed 3") 
	   elif event == ord(" "): 
	      screen.clear() 
	      screen.addstr("The User Pressed The Space Bar")
	
	for index, frameFilename in enumerate(filenames):
		hdulist = fits.open(frameFilename)
		imageData =  hdulist[0].data
		boostedImage = generalUtils.percentiles(imageData, 20, 99)
		ppgplot.pggray(boostedImage, 0, width-1, 0, height-1, 0, 255, imagePlot['pgPlotTransform'])
		outputFilename = outputDir + "/run-%04d.fits"%index
		hdulist.writeto(outputFilename, clobber=True)
		hdulist.close()
		time.sleep(readoutTime + exposureTime)
		screen.addstr("This is a Sample Curses Script\n\n") 
		
	
	ppgplot.pgclos()
	
	curses.endwin()
	
	
