#!/usr/bin/env python
# coding: UTF-8

# import
import serial
import sys
from datetime import datetime

from lib.pushbullet import push_message
from lib.twelite_PAL_parent import decode_PAL_data, print_PAL_data

## global conf ##
#monitoring type of each end device {EndDevice_Logical_ID:"TYPE"}
#TYPE :: WINDOW or MOISTURE
monitor_type = {1:"WINDOW", 2:"MOISTURE"}
#LOCATION
monitor_location = {1:"2Fベランダ窓", 2:"1F観葉植物"}

#
# window monitor
#
def logging_window_state(data_header, sensor_data):
	timestr = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
	path = "log/id"+str(data_header["EndDevice_Logical_ID"])+"_"+data_header["EndDevice_S/N"]+".csv"
	
	# data state
	for i in range(data_header["Sensor_N"]):
		if (sensor_data[i]["data_source"] == "Hall_IC") :
			hall_ic = sensor_data[i]["data"]
		if (sensor_data[i]["ext_byte"] == "Battery") :
			batt = sensor_data[i]["data"]
		if (sensor_data[i]["ext_byte"] == "ADC1") :
			adc1 = sensor_data[i]["data"]
	
	f = open(path, mode='a')
	f.write(timestr+", "+str(data_header["Sequence_Number"])+", "+str(data_header["LQI"])+", "+str(hall_ic)+", "+str(batt)+", "+str(adc1)+"\n")
	f.close()

def notify_window_state(data_header, sensor_data):
	global monitor_location

	timestr = datetime.now().strftime("%m/%d %H:%M:%S")
	time_hm = datetime.now().strftime("%H:%M")

	# location detection
	location = monitor_location[data_header["EndDevice_Logical_ID"]]

	# push notification when window is locked or unlocked
	for i in range(data_header["Sensor_N"]):
		if (sensor_data[i]["data_source"] == "Hall_IC") :
			mag_data = sensor_data[i]["data"]
			if (mag_data == 0):
				push_message(location, timestr+"にロックされました")
			elif (mag_data == 1) or (mag_data == 2):
				push_message(location, timestr+"にロックが解除されました")
		
		elif (sensor_data[i]["ext_byte"] == "Battery") :
			battV = sensor_data[i]["data"]
			if (time_hm == "21:30" and battV < 2300): 
				push_message(location, "バッテリー電圧低下 ("+str(battV)+"mV)")
	
	# periodic report
	if (time_hm == "22:00") :
		push_message(location+"(定期報告)", "sensor:"+str(mag_data)+"\nBattery:"+str(battV)+"mV \nLQI:"+str(data_header["LQI"]))

#
# soli moistture monitor
#
def logging_moisture_state(data_header, sensor_data):
	path = "log/id"+str(data_header["EndDevice_Logical_ID"])+"_"+data_header["EndDevice_S/N"]+".csv"
	
	timestr = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
	
	# data state
	for i in range(data_header["Sensor_N"]):
		if (sensor_data[i]["data_source"] == "Battery") :
			batt = sensor_data[i]["data"]
		if (sensor_data[i]["data_source"] == "AI1") :
			ai1 = sensor_data[i]["data"]
		if (sensor_data[i]["data_source"] == "AI2") :
			ai2 = sensor_data[i]["data"]
		if (sensor_data[i]["data_source"] == "AI3") :
			ai3 = sensor_data[i]["data"]
		if (sensor_data[i]["data_source"] == "AI4") :
			ai4 = sensor_data[i]["data"]
	
	f = open(path, mode='a')
	if data_header["Sensor_N"] == 3:
		f.write(timestr+", "+str(data_header["Sequence_Number"])+", "+str(data_header["LQI"])+", "+str(batt)+", "+str(ai1)+", "+str(ai2)+"\n")
	if data_header["Sensor_N"] == 5:
		f.write(timestr+", "+str(data_header["Sequence_Number"])+", "+str(data_header["LQI"])+", "+str(batt)+", "+str(ai1)+", "+str(ai2)+", "+str(ai3)+", "+str(ai4)+"\n")
	f.close()

def notify_moisture_state(data_header, sensor_data):
	global monitor_location

	location = monitor_location[data_header["EndDevice_Logical_ID"]]
	now = datetime.now()
	#timestr = datetime.now().strftime("%m/%d %H:%M:%S")

	# push notification when battery voltage is low
	for i in range(data_header["Sensor_N"]):
		if (sensor_data[i]["data_source"] == "AI1") :
			ai1 = sensor_data[i]["data"]
		if (sensor_data[i]["data_source"] == "AI2") :
			ai2 = sensor_data[i]["data"]
		if (sensor_data[i]["data_source"] == "AI3") :
			ai3 = sensor_data[i]["data"]
		if (sensor_data[i]["data_source"] == "AI4") :
			ai4 = sensor_data[i]["data"]
		if (sensor_data[i]["data_source"] == "Battery") :
			battV = sensor_data[i]["data"]
			if ((now.hour == 21) and (now.minute < 5)) and (battV < 2400): 
				push_message(location, "バッテリー電圧低下 ("+str(battV)+"mV)")
	
	# periodic report
	if (now.hour == 20) and (now.minute < 5) :
		if data_header["Sensor_N"] == 3:
			push_message(location+"(定期報告)", "Battery:"+str(battV)+"mV \nLQI:"+str(data_header["LQI"])+"\nAI1:"+str(ai1)+"\nAI2:"+str(ai2))
		if data_header["Sensor_N"] == 5:
			push_message(location+"(定期報告)", "Battery:"+str(battV)+"mV \nLQI:"+str(data_header["LQI"])+"\nAI1:"+str(ai1)+"\nAI2:"+str(ai2)+"\nAI3:"+str(ai3)+"\nAI4:"+str(ai4))

# main
def main():
	global monitor_type

	#serial port
	port_name = "/dev/ttyUSB0" #for linux
	#port_name = "COM4"        #for win
	
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
		sp = serial.Serial(port_name, 115200, timeout=0.1)
		print("open serial port: " + port_name)
	except:
		print("cannot open serial port: " + port_name)
		exit(1)
	
	print("starting TWE-LITE remote monitoring system...")
	while True:
		# read serial port (blocking) and strip EOL code 
		line = sp.readline().rstrip()

		if len(line) > 0 :
			#print("raw data (decodeed)  : " + line.decode())
			if line.decode()[0] == ":" :
				data_header, sensor_data = decode_PAL_data(line)
				if monitor_type[data_header["EndDevice_Logical_ID"]] == "WINDOW" : 
					notify_window_state(data_header, sensor_data)
					logging_window_state(data_header, sensor_data)
				elif monitor_type[data_header["EndDevice_Logical_ID"]] == "MOISTURE" : 
					notify_moisture_state(data_header, sensor_data)
					logging_moisture_state(data_header, sensor_data)
		else :
			continue
	
	sp.close()
	exit(0)
	
main()
