#!/usr/bin/env python
# coding: UTF-8

from serial import *
from sys import stdout, stdin, stderr, exit
import threading
from datetime import datetime

from lib.pushbullet import push_message
from lib.twelite_PAL import decode_PAL_data, print_PAL_data

#global setting
sp = None # serial port
t1 = None  # serial port reading thread
stopFlag = False # terminate flag

#port_name = "/dev/ttyUSB0" #default port
port_name = "COM3" #default port

def readThread():
	global sp, stopFlag
	while True:
		if stopFlag:
			return
		
		# read serial port (blocking) and strip EOL code 
		line = sp.readline().rstrip()

		if len(line) > 0 :
			#print("raw data (decodeed)  : " + line.decode())
			if line.decode()[0] == ":" :
				data_header, sensor_data = decode_PAL_data(line)
				print_PAL_data(data_header, sensor_data)
		else :
			continue

# terminate for serial port reading thread
def DoTerminate():
	global stopFlag
	stopFlag = True
	print ("... quitting")
	time.sleep(0.5) # waiting for thread termination
	exit(0)

# main
def main():
	global sp
	# arg check
	if len(sys.argv) == 1: #selected default port
		pass 
	elif len(sys.argv) != 2:
		print("illegal argument")
		exit(1)
	else:
		port_name = sys.argv[1]
	
	# open serial port
	try:
		sp = Serial(port_name, 115200, timeout=0.1)
		print ("open serial port: " + port_name)
	except:
		print ("cannot open serial port: " + port_name)
		exit(1)
	
	# start serial port reading thread
	t1=threading.Thread(target=readThread)
	t1.setDaemon(True)
	t1.start()
	print("reading thread started; waiting data...")
	print("type q to quit")
    
	# stdin
	while True:
		try:
			line_stdin = stdin.readline().rstrip()
			if len(line_stdin) > 0:
				if line_stdin[0] == 'q':
					DoTerminate()

		except KeyboardInterrupt: # Ctrl+C
			print("Detect pressing Ctrl+C")
			DoTerminate()
		except SystemExit:
			exit(0)
		except:
			print ("... unknown exception detected")
			break
	
	exit(0)
	
main()
