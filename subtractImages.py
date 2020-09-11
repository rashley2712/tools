#!/usr/bin/env python3

import argparse, os
from PIL import Image, ExifTags, ImageChops



if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Subtracts the second image from the first using the Image PIL library.')
	parser.add_argument('image1', type=str, help='First image.' )
	parser.add_argument('image2', type=str, help='Second image.' )
	parser.add_argument('-s', '--show', action='store_true', default=False, help='Show both images.' )
	parser.add_argument('--tags', action='store_true', default=False, help='Show the Exif tags.' )
	args = parser.parse_args()
	
	print("Python Image Library version:", Image.__version__)

	image1 = Image.open(args.image1)
	image2 = Image.open(args.image2)

	exif = image1.getexif()
	exif_dict = dict(exif)
	# { ... 42035: 'FUJIFILM', 42036: 'XF23mmF2 R WR', 42037: '75A14188' ... }
	exifData = {}
	for key, val in exif_dict.items():
		if key in ExifTags.TAGS:
			exifData[ExifTags.TAGS[key]] = val

	if args.tags:
		for k in exifData.keys():
			print(k)
    
	exposureTime = exifData['ExposureTime']
	print(args.image1, image1.bits, image1.size, image1.format, image1.mode, "Exposure time:", exposureTime)

	exifInterest = ['ExposureTime', 'ExposureMode', 'ShutterSpeedValue', 'FNumber']
	for e in exifInterest:
		print(e, exifData[e])

	if args.show: image1.show()
	else:
		thumbnailSize = tuple(x/8 for x in image1.size)
		preview = image1.copy()
		preview.thumbnail(thumbnailSize)
		preview.show()

	image3 = ImageChops.difference(image1, image2)	

	if args.show: image3.show()
	else:
		preview = image3.copy()
		preview.thumbnail(thumbnailSize)
		preview.show()

	filename = os.path.splitext(args.image1)[0] + "_darksubtracted.jpg"
	image3.save(filename)


