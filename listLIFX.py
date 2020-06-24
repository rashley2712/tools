import requests
import json

token = "c9d29aebfd2a9c0150fdab6ad4d614b72568cee8e12ad1994a8421b12021fd58"

headers = {
    "Authorization": "Bearer %s" % token,
}

response = requests.get('https://api.lifx.com/v1beta1/lights/all', headers=headers)

bulbs = json.loads(response.text)

print len(bulbs), "bulbs are registered."

connectedCount = 0
connectedBulbs = []
for b in bulbs:
	if b['connected'] == True:
		connectedCount+= 1
		connectedBulbs.append(b)
		print b['label'], "is connected!"
			
print "Number of connected bulbs", connectedCount


headers = {
    "Authorization": "Bearer %s" % token,
}

params = {
	"power": "off"
}

response = requests.put("https://api.lifx.com/v1beta1/lights/all/state", headers=headers, params=params)

raw_input("Press Enter to continue...")

params = {
	"power": "on"
}

response = requests.put("https://api.lifx.com/v1beta1/lights/all/state", headers=headers, params=params)

raw_input("Press Enter to continue...")

params = {
	"color": "kelvin:5000",
	"power_on": "true",
	"cycles": "5",
	"peak": "1"
}

testurl = "http://localhost"

response = requests.post("https://api.lifx.com/v1beta1/lights/all/effects/pulse", headers=headers, params=params)

print response.text

response = requests.put(testurl, headers=headers, params=params)
