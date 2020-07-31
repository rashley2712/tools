#!/usr/bin/env python3

import argparse, os, subprocess, sys, json, datetime, re, shutil
import HTMLdb

if __name__ == "__main__":
	
	parser = argparse.ArgumentParser(description='Archives all of the meteo images and updates the database.')
	parser.add_argument('-c','--config', type=str, default="", help='The config file.')
	parser.add_argument('-d','--date', type=str, default="yesterday", help='The date to archive. Defaults to yesterday.')
	parser.add_argument('-f','--find', action="store_true", default=False, help='Find all dates to archive (excluding today).')
	
	args = parser.parse_args()

	findFolders = False

	configFile = open(args.config, 'rt')
	config = json.loads(configFile.read())
	print(config)
	
	datesToArchive = []
	if args.find: 
		findFolders = True
		# Get a list of all folders matched the date format
		currentPath = config['HTMLPath']
		print("Finding all dates needing archive action in folder", currentPath)
		folders = [x[0] for x in os.walk(currentPath)]
		folders = [x.split('/')[-1] for x in folders]
		dateFolders = []
		for f in folders:
			m = re.search('\d{8}', f)
			if m is not None: dateFolders.append(f)
		print(dateFolders)
		now = datetime.datetime.now()
		todayDate = now.strftime("%Y%m%d")
		for d in dateFolders:
			if d!=todayDate: datesToArchive.append(d)

	elif args.date == 'yesterday':
		now = datetime.datetime.now()
		yesterday = now - datetime.timedelta(days=1)
		archiveDate = yesterday.strftime("%Y%m%d")
		print("No date specified ... going to archive yesterday, which was: :", archiveDate)
		datesToArchive = [archiveDate]
	else:
		archiveDate = args.date
		datesToArchive = [archiveDate]


	for archiveDate in datesToArchive:
		
		archiveFolder = os.path.join(config['HTMLPath'], archiveDate)
		
		archiveDestinationFolder = os.path.join(config['HTMLPath'], "archive")
		movieDestinationFolder = os.path.join(config['HTMLPath'], 'animations')
		if not os.path.exists(archiveDestinationFolder):
			os.mkdir(archiveDestinationFolder)
		if not os.path.exists(movieDestinationFolder):
			os.mkdir(movieDestinationFolder)

		# Get all the files in the folder
		fileCollection = []
		files = os.listdir(archiveFolder)
		mp4Files = []

		fileTypes = ['temp', 'humidity', 'cloud']
		
		for fileType in fileTypes: 
			matchedFiles = []
			movieFile = None
			for f in files:
				m = re.search('^' + fileType + '_.*\.png$', f)
				if m is not None: matchedFiles.append(f)
				m = re.search('_' + fileType + '\.gif$', f)
				if m is not None: movieFile = f

			if len(matchedFiles) == 0: continue
			matchedFiles = sorted(matchedFiles)
			tarFilename = archiveDate + "_" + fileType + ".tar.gz"
			os.chdir(archiveFolder)
			archiveCommand = ['tar']
			archiveCommand.append('czf')
			archiveCommand.append(tarFilename)
			archiveCommand+=matchedFiles
			subprocess.call(archiveCommand)
			print("Archived %d files to %s"%(len(matchedFiles), tarFilename))

			print("Moving to: ", archiveDestinationFolder)
			os.rename(tarFilename, os.path.join(archiveDestinationFolder, tarFilename))

			if movieFile is not None:
				print("Movie file is", movieFile)
				print("Moving to: ", movieDestinationFolder)
				os.rename(movieFile, os.path.join(movieDestinationFolder, movieFile))

		# Clean up and remove the existing folder
		shutil.rmtree(archiveFolder, ignore_errors=True)

		# Update the JSON db
		db = HTMLdb.HTMLdb()
		db.filename = config['dbFile']
		db.load()
		db.append('archivedDates', archiveDate)
		db.removeDuplicates('archivedDates')

		
