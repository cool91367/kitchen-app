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
import logging
import time
import json
import boto3
import RPi.GPIO as GPIO
import os
import glob
import re
import boto3
import base64
import requests
from io import BytesIO
# pip3 install pillow
from PIL import Image
# 
# s3 = boto3.client('s3',
#                   aws_access_key_id='ASIAUD2YPB2UWO4EDKWB',
#                     aws_secret_access_key= '77AzmPbwO6UA93zotqfDu/AXlSnsuyaW7Chg6nKW',
#                     aws_session_token= 'FwoGZXIvYXdzEOj//////////wEaDDXsDf8/ysVDaYD86CLJAV0xO4I8PBJaYenvhf0wZLbcmUGtwtjHLlM+YFCVwepAPislGkuHfG4uMPRHEuuvoCa4GkgP6Qsa5DeKy4oR+iCmhdRZ/bXZ+HfdaU8oWey3PHp4TnluhJgWC1zFYyytZmgpwnpAs6/iz6+iOZr1fUr3ZH2GX6NpBbG88pBWsUd4HXN/JwH1ceZ8TmuIj+WGlC/n/Q5m2y7nXswYWNPr6Kvo/6Nu+2jG/wIUTNqSD2GaZHSdV+IOJlcWnsNHgXrRfYokbcEEd1iLxijqtNL2BTIt4S/UYywjqh3YNymFhn1rt6jYRNzgZ/TjTtsxxXejjUKOet6tT0KPsVe+Nb2B'
#                   )

# Loop forever
camera = PiCamera()
camera.start_preview()

time.sleep(3)

camera.capture('/home/pi/Desktop/image.jpg')
camera.stop_preview()
image_path = "/home/pi/Desktop/image.jpg"
print(image_path)
img = Image.open(image_path)
img = img.resize((400, 200), Image.ANTIALIAS)
output_buffer = BytesIO()
img.save(output_buffer, format='JPEG')
byte_data = output_buffer.getvalue()
base64_str = base64.b64encode(byte_data)

# print(type(base64_str))
base64_str = base64_str.decode()
base64_str = base64_str.replace("/", ".")
base64_str = base64_str.replace("=", "_")
base64_str = base64_str.replace("+", "-")

url = "https://ez4kkdwqtk.execute-api.us-east-1.amazonaws.com/default/upload_image_to_s3"
myobj = {'image': base64_str}
re = requests.post(url, data = myobj)
print(re)

# try:
#     for i in range(5):
#         camera.start_preview()
# 
#         time.sleep(3)
# 
#         camera.capture('/home/pi/Desktop/image.jpg')
#         camera.stop_preview()
#         
#         
#         time.sleep(5)
# except KeyboardInterrupt:
#     print("Process shut down")



