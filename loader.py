#!/usr/bin/env python

import argparse
from PIL import Image 
import matplotlib.pyplot
import matplotlib.image
import numpy
import os, sys
import ppgplot
import PIL.ExifTags
import PIL.ImageChops
import scipy.signal
from scipy.fftpack import fft2, ifft2
from scipy.ndimage.fourier import fourier_shift
from scipy import ndimage

def phase_cor( A, B ):
  """
  find the 2D correlation between images A and B. This is much faster than any
  of the other scipy correlation methods which insist on working in the spatial
  domain.
  """
  return ( ifft2( fft2(A)*numpy.conj(fft2(B)) ) ).real

def apply_shift( X, shift ):
  """
  Shift an image in the fourier domain
  """
  return ifft2( fourier_shift( fft2(X), shift ) ).real


def getExifValue(image, tagName):
	try: 
		exif = {
	   		PIL.ExifTags.TAGS[k]: v
	    	for k, v in image._getexif().items()
	    	if k in PIL.ExifTags.TAGS
		}
	except AttributeError:
		return "unknown"
	
	try:
		tagValue = exif[tagName]
	except KeyError:
		tagValue = "unknown"
		
	return tagValue

if __name__ == "__main__":
	

	parser = argparse.ArgumentParser(description='Loads a series of jpeg files and displays them.')
	parser.add_argument('filelist', type=str, help='A text file containing a list of files to load')
	parser.add_argument('--dark', type=str, help='Subtract this dark frame from each image.' )

	args = parser.parse_args()
	
	print "Python Image Library version:", Image.VERSION
	
	files = open(args.filelist)
	filesToLoad = []
	for f in files:
		filename = f.strip()
		filesToLoad.append(filename)
	print "Files to load:", filesToLoad
	
	if args.dark!=None:
		print "loading a dark frame"
		dark = Image.open(args.dark)
		useDark = True
		# redDark, greenDark, blueDark = dark.split()
		# redDark, greenDark, blueDark = numpy.array(redDark), numpy.array(greenDark), numpy.array(blueDark)
	else:
		useDark = False
	
	images = []
	for f in filesToLoad:
		image = Image.open(f)
		print image.bits, image.size, image.format, image.mode
		exposureTime = getExifValue(image, 'ExposureTime')
		print "Exposure time:", exposureTime
		
		if useDark:
			image = PIL.ImageChops.difference(image, dark)
		
		images.append(image)
	
	(width, height) = images[0].size
	
	previewWindow = ppgplot.pgopen('/xs')	
	ppgplot.pgask(False)
	pgPlotTransform = [0, 1, 0, 0, 0, 1]
	ppgplot.pgsci(1)
	ppgplot.pgenv(0, width-1, 0, height-1, 0, 0)
	
	outputWindow = ppgplot.pgopen('/xs')	
	ppgplot.pgask(False)
	pgPlotTransform = [0, 1, 0, 0, 0, 1]
	ppgplot.pgsci(1)
	ppgplot.pgenv(0, width-1, 0, height-1, 0, 0)
	
	redReference = numpy.array(images[0].split()[0])
	redTotal = numpy.zeros(numpy.shape(redReference))
	greenTotal = numpy.zeros(numpy.shape(redReference))
	blueTotal = numpy.zeros(numpy.shape(redReference))
	
	for frameIndex, image in enumerate(images):
		redData, greenData, blueData = image.split()
		# redData.show()
		# print redData
		
		redData = numpy.array(redData)
		
		ppgplot.pgslct(previewWindow)
		ppgplot.pggray(redData, 0, width-1, 0, height-1, 0, 255, pgPlotTransform)
		
		# correlation = scipy.signal.correlate2d(redData, redReference, mode='same', boundary='symm')
		shift = phase_cor( redData, redReference)
		y, x = numpy.unravel_index(numpy.argmax(shift), shift.shape)
		if x > width/2:
			xd = width - x
		else: 
			xd = -x
		if y > height/2:
			yd = height - y
		else: 
			yd = -y
			
		print x, y, xd, yd
		
		shiftedImage = ndimage.interpolation.shift(redData, (yd, xd), order = 3 )
		redTotal+= shiftedImage
		greenTotal+= ndimage.interpolation.shift(greenData, (yd, xd), order = 3 )
		blueTotal+= ndimage.interpolation.shift(blueData, (yd, xd), order = 3 )
		redMax = numpy.max(redTotal)
		
		redScaled = redTotal / (frameIndex + 1)
		greenScaled = greenTotal / (frameIndex + 1)
		blueScaled = blueTotal / (frameIndex + 1)
		
		ppgplot.pgslct(outputWindow)
		ppgplot.pggray(redScaled, 0, width-1, 0, height-1, 255, 0, pgPlotTransform)
		
		redImage = Image.fromarray(redScaled)
		greenImage = Image.fromarray(greenScaled)
		blueImage = Image.fromarray(blueScaled)
		
		redImage = redImage.convert("L")
		greenImage = greenImage.convert("L")
		blueImage = blueImage.convert("L")
		#redImage.show()
		#greenImage.show()
		#blueImage.show()
		combinedImage = PIL.Image.merge('RGB', (redImage, greenImage, blueImage))
	
	combinedImage.save("output.jpg")	
	combinedImage.show()
		