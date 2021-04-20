#!/usr/bin/env python3

import argparse
import datetime
import datetime
import sys
import urllib.request
import os


# Google Cloud libraries
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from apiclient.http import MediaFileUpload


def getDriveListing():
		# Call the Drive v3 API
	results = service.files().list(
		pageSize=10, fields="nextPageToken, files(id, name)").execute()
	items = results.get('files', [])

	if not items:
		print('No files found.')
	else:
		print('Recent 10 files:')
		for item in items:
			print(u'{0} ({1})'.format(item['name'], item['id']))

def checkForExistingFile(service, name):
	print("Searching for a file called:", name)
	results = service.files().list(q="name = '" + name + "'", spaces="drive", fields="files(id, name, parents, trashed)").execute()
	if (len(results.get('files', [])) > 0): 
		print("file found!")
		allTrashed = True
		for f in results.get('files', []):
			print(f.get('name'), f.get('id'), f.get('parents'), f.get('trashed'))
			if not f.get('trashed'): return True
	return False


def uploadToDrive(crosswordFile):
	SCOPES = ['https://www.googleapis.com/auth/drive']
	creds = None
	if os.path.exists(cloudtokenFile):
		creds = Credentials.from_authorized_user_file(cloudtokenFile, SCOPES)
	else:
		print("No token.json file. Exiting")
		return

	service = build('drive', 'v3', credentials=creds)

	name = crosswordFile.split('/')[-1]
	if checkForExistingFile(service, name): return
	fileMetadata = { 'name': name, "parents" : ["1Kwy3lson-RWAntRkxO67NV-Mo6l8jYzw"]}
	media = MediaFileUpload(crosswordFile, mimetype='application/pdf')
	results = service.files().create(body=fileMetadata, media_body = media).execute()
	print("File Name: %s ID: %s"%(name, results.get('id')))


def getWriteCrossword(fullURL, outputFilename):
	try:
		response = urllib.request.urlopen(fullURL)
	except  urllib.error.HTTPError as e:
		print("We got an error of:", e.code)
		sys.exit()
	except urllib.error.URLError as e:
		print(e.reason)
		sys.exit()

	headers = str(response.headers)

	startIndex = headers.find('Content-Type')
	startIndex+= len("Content-Type: ")
	endIndex = headers.find('\n', startIndex)
	contentType = headers[startIndex:endIndex]
	# print("Content-type: " + contentType)
	if contentType!='application/pdf':
		print("The server did not return a PDF object.")
		sys.exit()

	pdfData = response.read()
	print("Fetched the data ok  ...  Writing to %s"%outputFilename)

	outputFile = open(outputFilename, 'wb')

	outputFile.write(pdfData)
	outputFile.close()

	print("Written the file to:", outputFilename)
	return outputFilename

if __name__ == "__main__":
	days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
	months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

	testBaseURL = "http://www.devicecloud.co.uk/crosswords/"
	baseURL = "http://crosswords-static.guim.co.uk/"
	homeDIR = os.getenv("HOME")
	crosswordPath = homeDIR + "/Crosswords/"
	namePrefix = "gdn.quick."
	nameSuffix = ".pdf"
	cloudtokenFile = homeDIR + "/bin/credentials.json"

	parser = argparse.ArgumentParser(description='Downloads the Guardian Quick crosswords and saves (and archives) them to a Dropbox folder.')
	parser.add_argument('--date', default = 'today', type=str, help='Date for the crossword (default: today)')
	parser.add_argument('-g', '--get', action='store_true', help='\'Get\' directive. Asks the script to get the crossword.')
	parser.add_argument('--test', action='store_true', help='Use the test URL instead of the real Guardian URL.')
	parser.add_argument('--archive', action = 'store_true', help='Clean up the Drive directory.')
	parser.add_argument('-u', '--upload', action = 'store_true', help='Upload the crossword to a Google Drive folder.')

	arg = parser.parse_args()
	print(arg)
	if arg.test:
		baseURL = testBaseURL


	todaysDate = datetime.datetime.now()
	requestedDate = todaysDate
	if arg.date!='today':
		try:
			inputDate = datetime.datetime.strptime(arg.date, '%Y-%m-%d')
			requestedDate = inputDate
		except ValueError:
			print("I am not able to understand the date input, please use YYYY-MM-DD")
			sys.exit()

	todayYear = todaysDate.year
	todayMonth = todaysDate.month
	todayDay = todaysDate.day
	todayDayOfWeek = todaysDate.weekday()

	requestedYear = requestedDate.year
	requestedDay = requestedDate.day
	requestedMonth = requestedDate.month
	requestedDayOfWeek = requestedDate.weekday()

	dayDifference = todaysDate - requestedDate

	print("Today is: %d-%02d-%02d %s"%(todayYear, todayMonth, todayDay, days[todayDayOfWeek]))
	print("You have asked for: %d-%02d-%02d %s"%(requestedYear, requestedMonth, requestedDay, days[requestedDayOfWeek]))
	if dayDifference.days<0:
		print("Your requested date is in the future, no crossword yet.")
		sys.exit()
	if dayDifference.days>0:
		print('Your date was %d days ago'%dayDifference.days)


	if requestedDayOfWeek == 6:
		print("You are requesting a crossword for a Sunday. Try the Observer.")
		sys.exit()

	dateString = "%d%02d%02d"%(requestedYear, requestedMonth, requestedDay)

	fullURL = baseURL + namePrefix + dateString + nameSuffix
	print("Ready to fetch: ", fullURL)
	outputFilename = crosswordPath + namePrefix + dateString + nameSuffix

	if (arg.get):
		crosswordFile = getWriteCrossword(fullURL, outputFilename)
	else:
		print("You did not specify the 'get' directive, so not really fetching the crossword.")

	if (arg.upload):
		uploadToDrive(crosswordFile)

	if (arg.archive):
		files = os.listdir(crosswordPath)
		crosswordFilenames = []
		dates = []
		for f in files:
			if f.find('gdn.quick.')!=-1:
				crosswordFilenames.append(f)
				dateString = f[10:18]
				dates.append(dateString)
		print("Crosswords found in root folder...")
		print(crosswordFilenames)
		daysOld = []
		for d in dates:
			date = datetime.datetime.strptime(d, '%Y%m%d')
			days = (todaysDate - date).days
			daysOld.append(days)

		oldCrosswords = []
		oldCrosswordDates = []
		for index, f in enumerate(crosswordFilenames):
			if daysOld[index] > 7:
				oldCrosswords.append(f)
				oldCrosswordDates.append(dates[index])

		print("Crosswords older than 7 days...")
		print(oldCrosswords)

		for index, filename in enumerate(oldCrosswords):
			date = datetime.datetime.strptime(oldCrosswordDates[index], '%Y%m%d')
			print(filename,date)
			month = date.month
			monthString = months[month-1]
			year = date.year
			print(year, monthString)
			directory = str(year) + "-" + monthString
			fullDirectory = dropboxPath + "/" + directory
			if not os.path.exists(fullDirectory):
				print("Creating the directory: " + fullDirectory)
				os.mkdir(fullDirectory)
			oldFilename = dropboxPath + "/" + filename
			newFilename = dropboxPath + "/" + directory + "/" + filename
			print(oldFilename, newFilename)
			os.rename(oldFilename, newFilename)


	print('Completed successfully')
