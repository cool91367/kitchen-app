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
#	"state": {
#		"desired":{
#			"property":<INT VALUE>
#		}
#	}
# }
s3 = boto3.client('s3',
                  aws_access_key_id='ASIAWQUDI2Q3HKICHLV3',
                    aws_secret_access_key= 'EjnD+qwFUpCARMrMdE61dNu+3IOCNzrBaTY7wtLM',
                    aws_session_token= 'FwoGZXIvYXdzEKP//////////wEaDN8n9mtWyVDQ1tuUbyLKAbKZR18gZhagSFrOToBXcCD0Gl6AdAutZKR5tv17dono8ANnOhdiMn0l+MlsfJlTpZhfJ+4vflxwbLRbfT463dog0qc7oAeMvVs72FDkH+/h8E/zjoLqPuoJECUsjkl73eWG6kPDQMLP6wTyFXDf4IypplCgzK94gpPSEI6pF9oCjIfPD8Ka9xM4OcDSMlWkHkPzQlhkWzhAgAxwjy25g0MBAzWUIIH7LinmPA35rkTwiKKt8eQPr1yMLarI1UdT4eyNdcTREKJpsksohbPD9gUyLcR0YjixaipROQz4456MOurblcuUZTbSgWklAPxGgUqz2urbKqhfllufQvw8xw=='
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
    else:
        print("off :(")
        GPIO.output(17,GPIO.LOW)


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
    
for i in range(5):
    camera.start_preview()

    time.sleep(3)

    camera.capture('/home/pi/Desktop/image2.jpg')
    camera.stop_preview()
    s3.upload_file('/home/pi/Desktop/image2.jpg', 'nthu-105062172', 'test1.jpg')
    
    time.sleep(5)
    

GPIO.cleanup()
