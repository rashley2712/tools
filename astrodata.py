#!/usr/bin/env python3
import ephem
#from datetime import date, datetime
import datetime

locations = [{ 
		"name" : "roque",
		"latitude" : 28.6468866, 
		"longitude" : -17.7742491,
		"elevation" : 2326 
	}, 
	{ 
		"name" : "sanjose",
		"latitude" : 28.6468866, 
		"longitude" : -17.7742491,
		"elevation" : 281 
	},
	{ 
		"name" : "madrid",
		"latitude" : 40.3719808, 
		"longitude" : -3.5262707,
		"elevation" : 900 
	}]

locationInfo = locations[2]

def information(text):
	print(text)

def getSunMoon(locationInfo): 
	night = False
	meteoLocation = ephem.Observer()
	meteoLocation.lon = str(locationInfo['longitude'])
	meteoLocation.lat = str(locationInfo['latitude'])
	meteoLocation.elevation = locationInfo['elevation']
	d = datetime.datetime.utcnow()
	localTime = ephem.localtime(ephem.Date(d))
	information("local time: " + str(localTime))
	information("universal time: " + str(d))
	meteoLocation.date = ephem.Date(d)
	sun = ephem.Sun(meteoLocation)
	moon = ephem.Moon(meteoLocation)
	information("Sun azimuth: %s altitude: %s"%(sun.az, sun.alt))
	altitude = sun.alt*180/3.14125
	information("Sun elevation is: %.2f"%altitude)
	currentDate = ephem.Date(d)
	timeToNewMoon = ephem.next_new_moon(currentDate) - currentDate
	timeSinceLastNewMoon = currentDate - ephem.previous_new_moon(currentDate)
	period = timeToNewMoon + timeSinceLastNewMoon
	phase = timeSinceLastNewMoon / period
	information("Moon elevation is: %.2f and illumination is: %.2f"%(moon.alt*180/3.14125, moon.phase))
	if phase>0.5:
		mode = "waning"
	else:
		mode = "waxing" 

	results = {
		"night" : night,
		"sunElevation" : altitude,
		"moonIllumination": moon.phase, 
		"moonElevation": (moon.alt*180/3.14125), 
		"moonMode": mode, 
		"phase" : phase
	}
	return results


jd = ephem.julian_date(ephem.now())

print(jd)

results = getSunMoon(locationInfo)
print(results)

sunout = open("/tmp/sun.log", "wt")
sunout.write("%2.1f"%results['sunElevation'])
sunout.close()

moonelout = open("/tmp/moonel.log", "wt")
moonelout.write("%2.1f"%results['moonElevation'])
moonelout.close()

moonphaseout = open("/tmp/moonil.log", "wt")
moonphaseout.write("%2.1f"%results['moonIllumination'])
moonphaseout.close()

moonmodeout = open("/tmp/moonmode.log", "wt")
moonmodeout.write(results['moonMode'])
moonmodeout.close()

moonSymbols = [ u'🌑', u'🌒', u'🌓', u'🌔', u'🌕', u'🌖', u'🌗', u'🌘' ]

symbolIndex = round(results['phase']*8)
if symbolIndex > 7: symbolIndex = 0
print(results['phase'], symbolIndex, moonSymbols[symbolIndex])

moonsymbolout = open("/tmp/moonsymbol.log", "wt")
moonsymbolout.write(moonSymbols[symbolIndex])
moonsymbolout.close()


jdout = open("/tmp/jd.log", "wt")
jdout.write("%.4f"%jd)
jdout.close()
