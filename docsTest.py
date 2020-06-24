import json
import gspread
from oauth2client.client import SignedJwtAssertionCredentials
from oauth2client.client import flow_from_clientsecrets

json_key = json.load(open('rashley-68ec4c63b5c5.json'))
scope = ['https://spreadsheets.google.com/feeds']

credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'], scope)

gc = gspread.authorize(credentials)
print gc


allSheets = gc.openall(title=None)
print "Number of sheets found:", len(allSheets)
for a in allSheets:
	print a



# wks = gc.open("Where is the money Lebowski?").sheet1

wks = gc.open_by_key('1R5ozji9TjmxU04rNUDJKz3fah9oKiVF9P6KPQikbBgo')