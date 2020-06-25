#!/usr/bin/env python3

import argparse, os, subprocess
import sys
import datetime
import HTMLdb, json

if __name__ == "__main__":
	
	parser = argparse.ArgumentParser(description='Makes the animation of the latest files.')
	parser.add_argument('-c','--config', type=str, default="", help='The config file.')
	
	args = parser.parse_args()

	configFile = open(args.config, 'rt')
	config = json.loads(configFile.read())
	print(config)

	db = HTMLdb.HTMLdb()
	db.filename = config['dbFile']
	db.load()

	now = datetime.datetime.now()
	timeString = now.strftime("%Y%m%d_%H%M")
	dateString = now.strftime("%Y%m%d")
	folder = os.path.join(config['HTMLPath'], dateString)

	# Generate the list of files in today's folder
	fileCollection = []
	files = os.listdir(folder)
	for f in files:
		if f.startswith("temp"):
			fileCollection.append(f)

	fileCollection = sorted(fileCollection)
	print(fileCollection)
	
	listFile = open(os.path.join(folder, "%s_temp.list"%dateString), 'wt')
	for f in fileCollection:
		listFile.write("%s\n"%f)
	listFile.close()
	user = os.getlogin()
	ffmpegCommand = ["/home/%s/bin/pipeFFMPEG.bash"%user]
	ffmpegCommand.append(dateString + "_temp")
	print("Running:", ffmpegCommand)
	from subprocess import Popen, PIPE
	#output, errors = Popen(archiveFolder, stdout=PIPE, stderr=PIPE).communicate()
	os.chdir(folder)
	subprocess.call(ffmpegCommand)

	# os.rename(os.path.join(archiveFolder, yesterdayString+".mp4"), os.path.join(args.outputpath, yesterdayString + ".mp4"))

	# Now generate an animated gif from the mp4
	# ffmpeg -i 20200622.mp4 -filter_complex "[0:v] split [a][b];[a] palettegen [p];[b][p] paletteuse" out.gif

	ffmpegCommand = ['ffmpeg']
	ffmpegCommand.append('-y')
	ffmpegCommand.append('-i')
	ffmpegCommand.append(dateString + "_temp.mp4")
	ffmpegCommand.append('-filter_complex')
	ffmpegCommand.append('[0:v] split [a][b];[a] palettegen [p];[b][p] paletteuse')
	ffmpegCommand.append(dateString + '_temp.gif')
	print(ffmpegCommand)
	subprocess.call(ffmpegCommand)
	db.set("latestTempVideo", os.path.join(config["webRoot"], dateString, dateString + "_temp.gif"))

	# Generate the list of files in today's folder
	fileCollection = []
	files = os.listdir(folder)
	for f in files:
		if f.startswith("humidity"):
			fileCollection.append(f)

	fileCollection = sorted(fileCollection)
	print(fileCollection)
	
	listFile = open(os.path.join(folder, "%s_humidity.list"%dateString), 'wt')
	for f in fileCollection:
		listFile.write("%s\n"%f)
	listFile.close()
	user = os.getlogin()
	ffmpegCommand = ["/home/%s/bin/pipeFFMPEG.bash"%user]
	ffmpegCommand.append(dateString + "_humidity")
	print("Running:", ffmpegCommand)
	from subprocess import Popen, PIPE
	#output, errors = Popen(archiveFolder, stdout=PIPE, stderr=PIPE).communicate()
	os.chdir(folder)
	subprocess.call(ffmpegCommand)

	# os.rename(os.path.join(archiveFolder, yesterdayString+".mp4"), os.path.join(args.outputpath, yesterdayString + ".mp4"))

	# Now generate an animated gif from the mp4
	# ffmpeg -i 20200622.mp4 -filter_complex "[0:v] split [a][b];[a] palettegen [p];[b][p] paletteuse" out.gif

	ffmpegCommand = ['ffmpeg']
	ffmpegCommand.append('-y')
	ffmpegCommand.append('-i')
	ffmpegCommand.append(dateString + "_humidity.mp4")
	ffmpegCommand.append('-filter_complex')
	ffmpegCommand.append('[0:v] split [a][b];[a] palettegen [p];[b][p] paletteuse')
	ffmpegCommand.append(dateString + '_humidity.gif')
	print(ffmpegCommand)
	subprocess.call(ffmpegCommand)
	db.set("latestHumidityVideo", os.path.join(config["webRoot"], dateString, dateString + "_humidity.gif"))

	# CLOUD
	# Generate the list of files in today's folder
	fileCollection = []
	files = os.listdir(folder)
	for f in files:
		if f.startswith("cloud"):
			fileCollection.append(f)

	fileCollection = sorted(fileCollection)
	print(fileCollection)
	
	listFile = open(os.path.join(folder, "%s_cloud.list"%dateString), 'wt')
	for f in fileCollection:
		listFile.write("%s\n"%f)
	listFile.close()
	user = os.getlogin()
	ffmpegCommand = ["/home/%s/bin/pipeFFMPEG.bash"%user]
	ffmpegCommand.append(dateString + "_cloud")
	print("Running:", ffmpegCommand)
	from subprocess import Popen, PIPE
	os.chdir(folder)
	subprocess.call(ffmpegCommand)

	ffmpegCommand = ['ffmpeg']
	ffmpegCommand.append('-y')
	ffmpegCommand.append('-i')
	ffmpegCommand.append(dateString + "_cloud.mp4")
	ffmpegCommand.append('-filter_complex')
	ffmpegCommand.append('[0:v] split [a][b];[a] palettegen [p];[b][p] paletteuse')
	ffmpegCommand.append(dateString + '_cloud.gif')
	print(ffmpegCommand)
	subprocess.call(ffmpegCommand)
	db.set("latestCloudVideo", os.path.join(config["webRoot"], dateString, dateString + "_cloud.gif"))
	sys.exit()

