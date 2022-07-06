import requests
print("Uploading data")
success = False
destination = "https://skywatching.eu/meteo"
print("Uploading to ", destination)
myobj = {'logData': "some information"}
print(myobj)
try: 
	x = requests.post(destination, data = myobj)
	print(x.text)
	if x.text == "SUCCESS": success = True
	x.close()
except Exception as e: 
	success = False
	print(e)
				

