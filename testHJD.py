#!/usr/bin/env python3
import argparse
import datetimelib
import numpy


if __name__ == "__main__":
	
	parser = argparse.ArgumentParser(description='Converts HJD to JD.')
	#parser.add_argument('file', type=str, help='Input filename.')
	#parser.add_argument('-o', '--output', type=str, help="")
	args = parser.parse_args()


	ephem = datetimelib.ephemerisObject()
	ephem.loadFromFile('/home/rashley/drive/astronomy/CRTS2152/ephemeris.dat')
	print(ephem)
	
	helio = datetimelib.heliocentric()
	helio.setTelescope('WHT')
	helio.setTarget(ephem.ra, ephem.dec)

	HJDs = []
	for orbit in range(7095, 7100):
		HJD = ephem.T0 + ephem.Period * orbit
		print("orbit: %d  HJD:%f"%(orbit, HJD))
		HJDs.append(HJD)

	JDs = helio.convertHJDtoJD(HJDs)
	print(JDs)
		