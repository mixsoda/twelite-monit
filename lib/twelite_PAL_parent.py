#!/usr/bin/env python
# coding: UTF-8

def decode_PAL_data(line):
	#init data store
	data_header = {}
	sensor_data = list()

	#installed applist of each end device
	installed_app = {1:"PAL", 2:"TAG"}

	ld = line.decode()
	print(ld)

	#data header
	data_header["Repeater_ID"] = ld[1:9]
	data_header["LQI"] = int(ld[9:11],16)
	data_header["Sequence_Number"] = int(ld[11:15],16)
	data_header["EndDevice_S/N"] = ld[15:23]
	data_header["EndDevice_Logical_ID"] = int(ld[23:25],16)

	if installed_app[data_header["EndDevice_Logical_ID"]] == "PAL" :

		data_header["Sensor_Type"] = ld[25:27]
		data_header["Sensor_N"] = int(ld[29:31],16)

		module_type = int(str(int(ld[27:29],16) & 0x1F),2)
		if module_type == 0 :
			data_header["Module_Type"] = "NOT_CONNECT"
		elif module_type == 1 :
			data_header["Module_Type"] = "MAG"
		elif module_type == 2 :
			data_header["Module_Type"] = "AMB"
		elif module_type == 3 :
			data_header["Module_Type"] = "MOT"
		else:
			data_header["Module_Type"] = "UNKNOWN"

		j=31
		for i in range(data_header["Sensor_N"]):
			meta_data = int(ld[j:j+2],16)
			data_source = int(ld[j+2:j+4],16)
			ext_byte = int(ld[j+4:j+6],16)
			data_length = int(ld[j+6:j+8],16)
			data = int(ld[j+8:j+8+2*data_length],16)

			read_error = (meta_data>>7 & 1)
			ext_byte_flag = (meta_data>>4 & 1)
			negative_sign = (meta_data>>2 & 1)
			data_type = int(str(meta_data & 0x3),2)

			if(data_source == 0): data_source = "Hall_IC"
			if(data_source == 1): data_source = "Temp"
			if(data_source == 2): data_source = "Hu"
			if(data_source == 3): data_source = "Li"
			if(data_source == 4): data_source = "Acc"
			if(data_source == 48): data_source = "Voltage"
			if(data_source == 49): data_source = "DIO"
			if(data_source == 50): data_source = "EEPROM"
			
			if(data_source == "Voltage"):
				if(ext_byte == 1): ext_byte = "ADC1"
				if(ext_byte == 2): ext_byte = "ADC2"
				if(ext_byte == 3): ext_byte = "ADC3"
				if(ext_byte == 4): ext_byte = "ADC4"
				if(ext_byte == 8): ext_byte = "Battery"

			sensor_data.append({"read_error":read_error, "ext_byte_flag":ext_byte_flag, "negative_sign":negative_sign, "data_type":data_type, "data_source":data_source, "ext_byte":ext_byte, "data_length":data_length, "data":data})
			j=31+(i+1)*(8+2*data_length)
	
	elif installed_app[data_header["EndDevice_Logical_ID"]] == "TAG" :
		data_header["Module_Type"] = "TAG"
		sensor_type = int(ld[25:27],16)
		data_header["Sensor_N"] = 5
		if(sensor_type == 16): data_header["Sensor_Type"]  = "ANALOG"
		if(sensor_type == 17): data_header["Sensor_Type"]  = "LM61"
		if(sensor_type == 49): data_header["Sensor_Type"]  = "SHT21"
		if(sensor_type == 50): data_header["Sensor_Type"]  = "ADT7410"
		if(sensor_type == 51): data_header["Sensor_Type"]  = "MPL115A2"
		if(sensor_type == 52): data_header["Sensor_Type"]  = "LIS3DH"
		if(sensor_type == 53): data_header["Sensor_Type"]  = "ADXL34x"
		if(sensor_type == 54): data_header["Sensor_Type"]  = "TSL2561"
		if(sensor_type == 55): data_header["Sensor_Type"]  = "L3GD20"
		if(sensor_type == 56): data_header["Sensor_Type"]  = "S11059-02DT"
		if(sensor_type == 57): data_header["Sensor_Type"]  = "BME280"
		if(sensor_type == 58): data_header["Sensor_Type"]  = "SHT3x"
		if(sensor_type == 59): data_header["Sensor_Type"]  = "SHTC1"
		if(sensor_type == 97): data_header["Sensor_Type"]  = "MAX31855"
		if(sensor_type == 209): data_header["Sensor_Type"]  = "MULTI_SENSOR"
		if(sensor_type == 254): data_header["Sensor_Type"]  = "PUSH_BUTTON"

		if data_header["Sensor_Type"]  == "ANALOG" :
			ai1 = int(ld[29:33],16)
			ai2 = int(ld[33:37],16)
			ai3 = int(ld[37:41],16)
			ai4 = int(ld[41:45],16)
			if ai1 >= int(hex(0x8000),16) :
				data_header["Sensor_N"] = 5
				ai1 = ai1 - int(hex(0x8000),16)
				sensor_data.append({"data_source":"AI3", "data":ai3})
				sensor_data.append({"data_source":"AI4", "data":ai4})
			else:
				data_header["Sensor_N"] = 3
			sensor_data.append({"data_source":"AI1", "data":ai1})
			sensor_data.append({"data_source":"AI2", "data":ai2})

			battV_HEX = int(ld[27:29],16)
			if(battV_HEX <= 170) :
				battV = 1950+battV_HEX*5
			else :
				battV = 2800+(battV_HEX-170)*10
			sensor_data.append({"data_source":"Battery", "data":battV})

	return data_header, sensor_data	

def print_PAL_data(data_header, sensor_data):
	print("Repeater ID          : " + data_header["Repeater_ID"])
	print("LQI                  : " + str(data_header["LQI"]))
	print("Sequence Number      : " + str(data_header["Sequence_Number"]))
	print("EndDevice S/N        : " + data_header["EndDevice_S/N"])
	print("EndDevice Logical ID : " + str(data_header["EndDevice_Logical_ID"]))
	print("Sensor Type(PAL=80)  : " + data_header["Sensor_Type"])
	print("Module / Version     : " + str(data_header["Module_Type"]))
	print("Number of sensors    : " + str(data_header["Sensor_N"]))
	print("")
	print("sensor data")
	for i in range(data_header["Sensor_N"]):
		print(sensor_data[i])
	print("")