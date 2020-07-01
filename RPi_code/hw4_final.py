'''
/*
 * Copyright 2010-2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.
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
from picamera import PiCamera
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
import logging
import time
import json
import argparse
import RPi.GPIO as GPIO
import boto3

GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.OUT)

# Shadow JSON schema:
#
# Name: Bot
# {
#   "state": {
#       "desired":{
#           "property":<INT VALUE>
#       }
#   }
# }
s3 = boto3.client('s3',
                  aws_access_key_id='ASIAWQUDI2Q3LJCY6H7L',
                    aws_secret_access_key= 'BpmpXg0bJP4VatPYQl+Qtuhc3ksSmJVoIvyyhpZ6',
                    aws_session_token= 'FwoGZXIvYXdzEJD//////////wEaDGtL1ecB/QHJv0DbHSLKAaEoGHagElkHrEQjJCU6765yirBXZ/YpVZJpZmfgN4crpLFuAHpiYuhohHFJEzQXL7qffoL5J4oSLVSfYNWMnEIlhGLokZjlDl1FeNti9qzM82AGLYx8mwiO91Ru21dCQbJJW7xvUbdVX7n0Bi7iUTvsMzx9JvBz0jHo1TYa4rINH5XTUfpjqZpEkX6c81mLIS3gmB0dm9+8wI8z5eVL3EEuxJJc8zG21nsC1cZ0Jkh5e+XwOnqxaphgqhDJ4joN89UhEZopcie18QEo2sL39gUyLRzoygmIVVnrip9y/dHExC8+6cJBG8rO77cH7jVK3T0I2rJ4z0qM/rymqJg3wg=='
                  )


# Custom Shadow callback
def customShadowCallback_Delta(payload, responseStatus, token):
    # payload is a JSON string ready to be parsed using json.loads(...)
    # in both Py2.x and Py3.x
    print(responseStatus)
    payloadDict = json.loads(payload)
    print("++++++++DELTA++++++++++")
    print("light: " + str(payloadDict["state"]["light"]))
    #print("version: " + str(payloadDict["version"]))
    print("+++++++++++++++++++++++\n\n")
    
    if(payloadDict["state"]["light"] == 1):
        print("bulb on :)")
        GPIO.output(17,GPIO.HIGH)
        JSONPayload = '{"state":{"reported":{"light": 1 }}}'
        deviceShadowHandler.shadowUpdate(JSONPayload, customShadowCallback_Update, 5)
    
    else:
        print("off :(")
        GPIO.output(17,GPIO.LOW)
        JSONPayload = '{"state":{"reported":{"light": 0 }}}'
        deviceShadowHandler.shadowUpdate(JSONPayload, customShadowCallback_Update, 5)

def customShadowCallback_Update(payload, responseStatus, token):
    # payload is a JSON string ready to be parsed using json.loads(...)
    # in both Py2.x and Py3.x
    if responseStatus == "timeout":
        print("Update request " + token + " time out!")
    if responseStatus == "accepted":
        payloadDict = json.loads(payload)
        print("~~~~~~~~~~~~~~~~~~~~~~~")
        print("Update request with token: " + token + " accepted!")
        print("property: " + str(payloadDict["state"]["reported"]["light"]))
        print("~~~~~~~~~~~~~~~~~~~~~~~\n\n")
    if responseStatus == "rejected":
        print("Update request " + token + " rejected!")

# Read in command-line parameters
parser = argparse.ArgumentParser()
parser.add_argument("-e", "--endpoint", action="store", required=True, dest="host", help="Your AWS IoT custom endpoint")
parser.add_argument("-r", "--rootCA", action="store", required=True, dest="rootCAPath", help="Root CA file path")
parser.add_argument("-c", "--cert", action="store", dest="certificatePath", help="Certificate file path")
parser.add_argument("-k", "--key", action="store", dest="privateKeyPath", help="Private key file path")
parser.add_argument("-p", "--port", action="store", dest="port", type=int, help="Port number override")
parser.add_argument("-w", "--websocket", action="store_true", dest="useWebsocket", default=False,
                    help="Use MQTT over WebSocket")
parser.add_argument("-n", "--thingName", action="store", dest="thingName", default="Bot", help="Targeted thing name")
parser.add_argument("-id", "--clientId", action="store", dest="clientId", default="basicShadowDeltaListener",
                    help="Targeted client id")



host = 'aifc1a3xa2vzj-ats.iot.us-east-1.amazonaws.com'
rootCAPath = '/home/pi/Desktop/root-CA.crt'
certificatePath = '/home/pi/Desktop/hw4.cert.pem'
privateKeyPath = '/home/pi/Desktop/hw4.private.key'
useWebsocket = False
clientId = 'basicShadowDeltaListener'
port = 8883
GPIO.output(17,GPIO.LOW)

# Configure logging
logger = logging.getLogger("AWSIoTPythonSDK.core")
logger.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

# Init AWSIoTMQTTShadowClient
myAWSIoTMQTTShadowClient = None
if useWebsocket:
    myAWSIoTMQTTShadowClient = AWSIoTMQTTShadowClient(clientId, useWebsocket=True)
    myAWSIoTMQTTShadowClient.configureEndpoint(host, port)
    myAWSIoTMQTTShadowClient.configureCredentials(rootCAPath)
else:
    myAWSIoTMQTTShadowClient = AWSIoTMQTTShadowClient(clientId)
    myAWSIoTMQTTShadowClient.configureEndpoint(host, port)
    myAWSIoTMQTTShadowClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

# AWSIoTMQTTShadowClient configuration
myAWSIoTMQTTShadowClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTShadowClient.configureConnectDisconnectTimeout(20)  # 10 sec
myAWSIoTMQTTShadowClient.configureMQTTOperationTimeout(5)  # 5 sec

# Connect to AWS IoT
myAWSIoTMQTTShadowClient.connect()

# Create a deviceShadow with persistent subscription
deviceShadowHandler = myAWSIoTMQTTShadowClient.createShadowHandlerWithName('hw4', True)

# Listen on deltas
deviceShadowHandler.shadowRegisterDeltaCallback(customShadowCallback_Delta)

# Loop forever
camera = PiCamera()

#while True:
    
for i in range(3):
    camera.start_preview()

    time.sleep(3)

    camera.capture('/home/pi/Desktop/image2.jpg')
    camera.stop_preview()
    s3.upload_file('/home/pi/Desktop/image2.jpg', 'nthu-105062172', 'test1.jpg')
    
    time.sleep(3)
    

GPIO.cleanup()

