'''
/*
 * Copyright 2010-2016 Amazon.com, Inc. or its affiliates. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License").
 * You may not use this file except in compliance with the License.
 * A copy of the License is located at
 *
 *  http://aws.amazon.com/apache2.0
 *
 * or in the "license" file accompanying this file. This file is distributed
 * on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
 * express or implied. See the License for the specific language governing
 * permissions and limitations under the License.
 */
'''

import sys
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging
import time
import getopt
import os
import subprocess
import json
import commands
sys.path.append('/home/pi/SBC-SDK-PYTHON')
from config import *
import RPi.GPIO as GPIO
from pprint import pprint
from uuid import getnode as get_mac
import serial

GPIO.setmode(GPIO.BCM)

ser = serial.Serial("/dev/ttyUSB0",9600)
ser.isOpen()

# Custom MQTT message callback
def customCallback(client, userdata, message):
		print("Received a new message:----------->>>> ")
		print(message.payload)
		print("from topic: ")
		print(message.topic)
		print("	--------------\n\n")
		subscribeMsg = (message.payload)	
		for i in range(0, len(subscribeMsg)):
				if subscribeMsg[i] == ' ':
					myFeed = subscribeMsg[0:i]
					myStatus = subscribeMsg[i+1:len(subscribeMsg)]
		print("*********************")
		print(myFeed)
		print(myStatus)
		print("*********************")

		if myFeed == controlfeedname1:
			if myStatus == "on" or myStatus == "ON":
			 		ser.write("GPIO 1 ON*")
	 		elif myStatus == "off" or myStatus == "OFF" :
	 				ser.write("GPIO 1 OFF*")
		elif myFeed == controlfeedname2 :
			if myStatus == "on" or myStatus == "ON":
	 				ser.write("GPIO 2 ON*")
			elif myStatus == "off" or myMsg == "OFF" :
					ser.write("GPIO 2 OFF*")

    		'''j = json.loads(message.payload)
		pprint(j['Type'])
	 	if(j['Type']=="publish"):
	 		gpio = j['gpio']
	 		status = j['status']'''




# Usage
	 	usageInfo = """Usage:

		Use certificate based mutual authentication:
	 	python basicPubSub.py -e <endpoint> -r <rootCAFilePath> -c <certFilePath> -k <privateKeyFilePath>

	 	Use MQTT over WebSocket:
		python basicPubSub.py -e <endpoint> -r <rootCAFilePath> -w

	 	Type "python basicPubSub.py -h" for available options.
	 	"""
# Help info
		helpInfo = """-e, --endpoint
	 	Your AWS IoT custom endpoint
	 	-r, --rootCA
	 	Root CA file path
	 	-c, --cert
	 	Certificate file path
	 	-k, --key
		Private key file path
		-w, --websocket
	 	Use MQTT over WebSocket
	 	-h, --help
	 	Help information


		"""	

# Read in command-line parameters
useWebsocket = False
host = "a3rwl3kghmkdtx.iot.us-west-2.amazonaws.com"
rootCAPath = "/home/pi/SBC-SDK-PYTHON/certs/rootCA.crt"
certificatePath = "/home/pi/SBC-SDK-PYTHON/certs/e76b102a41-certificate.pem.crt"
privateKeyPath = "/home/pi/SBC-SDK-PYTHON/certs/e76b102a41-private.pem.key"


# Missing configuration notification
missingConfiguration = False
if not host:
	 print("Missing '-e' or '--endpoint'")
	 missingConfiguration = True
	 if not rootCAPath:
	 	print("Missing '-r' or '--rootCA'")
	 	missingConfiguration = True
	 if not useWebsocket:
	 	if not certificatePath:
	 		print("Missing '-c' or '--cert'")
	 		missingConfiguration = True
	 if not privateKeyPath:
	 	print("Missing '-k' or '--key'")
		missingConfiguration = True
	 if missingConfiguration:
		exit(2)

# Configure logging
logger = logging.getLogger("AWSIoTPythonSDK.core")
logger.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

# Init AWSIoTMQTTClient
myAWSIoTMQTTClient = None
if useWebsocket:
	myAWSIoTMQTTClient = AWSIoTMQTTClient("basicPubSub", useWebsocket=True)
	myAWSIoTMQTTClient.configureEndpoint(host, 443)
	myAWSIoTMQTTClient.configureCredentials(rootCAPath)
else:
	myAWSIoTMQTTClient = AWSIoTMQTTClient("basicPubSub")
	myAWSIoTMQTTClient.configureEndpoint(host, 8883)
	myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

# AWSIoTMQTTClient connection configuration
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(100)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(50)  # 5 sec

# Connect and subscribe to AWS IoT
myAWSIoTMQTTClient.connect()
myAWSIoTMQTTClient.subscribe(UserName+"_"+DeviceName, 1, customCallback)
time.sleep(5)

# Publish to the same topic in a loop forever
loopCount = 0
MyMac = open('/sys/class/net/eth0/address').read()
MyMac = MyMac[0:len(MyMac)-1]

jsonbasestring = """{"feedname1" : """+"\""+feedname1+"\""+""",
"feedname2" : """+"\""+feedname2+"\""+""",
"feedname3" : """+"\""+feedname3+"\""+""",
"feedname4" : """+"\""+feedname4+"\""+""",
"feedname5" : """+"\""+controlfeedname1+"\""+""",
"feedname6" : """+"\""+controlfeedname2+"\""+""",
"username" : """+"\""+UserName+"\""+""",
"devicename" : """+"\""+DeviceName+"\""+""",
"paasmerid" : """+"\""+MyMac+"\""+"""
}"""

def sensor_read(n):
	list1=str()
	if n==1:
		ser.write("Read pin 1*")
		time.sleep(0.5)
		incoming=ser.read()
		if incoming == '*':
			print(incoming)
		else:
			list1=list1+incoming
			print(incoming)
			
	elif n==2:
		ser.write("Read pin 2*")
		time.sleep(0.5)
        	incoming=ser.read()
       		if incoming == '*':
			print(incoming)
               	else:
                	list1=list1+incoming
			print(incoming)
                  	
	elif n==3:
       			ser.write("Read pin 3*")
			time.sleep(0.5)
	 	      	incoming=ser.read()
               		if incoming == '*':
				print(incoming)
       			else:
				list1=list1+incoming
				print(incoming)

	elif n==4:
			ser.write("Read pin 4*")
			time.sleep(0.5)
			incoming=ser.read()
			if incoming == '*':
				print(incoming)
			else:
				list1=list1+incoming
				print(incoming)

	return incoming

myAWSIoTMQTTClient.publish("paasmer_device_details",jsonbasestring, 1)
while True :
	s1_out = sensor_read(1)
	time.sleep(2)
	s2_out = sensor_read(2)
	time.sleep(2)
	s3_out = sensor_read(3)
	time.sleep(2)
	s4_out = sensor_read(4)
	time.sleep(2)			
 
	jsonstring = """{"feedname1" : """+"\""+feedname1+"\""+""",
	"feedname2" : """+"\""+feedname2+"\""+""",
	"feedname3" : """+"\""+feedname3+"\""+""",
	"feedname4" : """+"\""+feedname4+"\""+""",
	"sensorvalue1" : """+"\""+str(s1_out)+"\""+""", 
	"sensorvalue2" : """+"\""+str(s2_out)+"\""+""", 
	"sensorvalue3" : """+"\""+str(s3_out)+"\""+""", 
	"sensorvalue4" : """+"\""+str(s4_out)+"\""+""", 
	"username" : """+"\""+UserName+"\""+""",
	"devicename" : """+"\""+DeviceName+"\""+""",
	"paasmerid" : """+"\""+MyMac+"\""+"""
	}"""

	myAWSIoTMQTTClient.publish("paasmer_sensor_details",jsonstring, 1)
	loopCount += 1
	time.sleep(timePeriod)

