#!/usr/bin/env python
# coding: UTF-8

#import
import requests
import json

def push_message(title, body):
	token = "YOUR PRIVATE TOKEN IS HERE"
	url = "https://api.pushbullet.com/v2/pushes"
	
	headers = {"content-type": "application/json", "Authorization": 'Bearer '+token}
	data_send = {"type": "note", "title": title, "body": body}

	_r = requests.post(url, headers=headers, data=json.dumps(data_send))