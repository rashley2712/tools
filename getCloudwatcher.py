#!/usr/bin/env python3

import argparse, os, io
from serial import Serial
		
if __name__ == "__main__":
	
	parser = argparse.ArgumentParser(description='Talks to the Cloudwatcher via the serial port.')
	args = parser.parse_args()

	ser = Serial('/dev/ttyUSB0')  # open serial port
	ser.baudrate = 9600
	print(ser.name)         # check which port was really used
	
	sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))
	sio.write("A!\n")
	sio.flush() # it is buffering. required to get the data out *now*
	hello = sio.read()
	print(hello)
	
	ser.close()        

	
