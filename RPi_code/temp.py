import os
import glob
import time
import RPi.GPIO as GPIO
import json
import boto3
db = boto3.client('dynamodb',
                  aws_access_key_id='ASIAUD2YPB2UWO4EDKWB',
                    aws_secret_access_key= '77AzmPbwO6UA93zotqfDu/AXlSnsuyaW7Chg6nKW',
                    aws_session_token= 'FwoGZXIvYXdzEOj//////////wEaDDXsDf8/ysVDaYD86CLJAV0xO4I8PBJaYenvhf0wZLbcmUGtwtjHLlM+YFCVwepAPislGkuHfG4uMPRHEuuvoCa4GkgP6Qsa5DeKy4oR+iCmhdRZ/bXZ+HfdaU8oWey3PHp4TnluhJgWC1zFYyytZmgpwnpAs6/iz6+iOZr1fUr3ZH2GX6NpBbG88pBWsUd4HXN/JwH1ceZ8TmuIj+WGlC/n/Q5m2y7nXswYWNPr6Kvo/6Nu+2jG/wIUTNqSD2GaZHSdV+IOJlcWnsNHgXrRfYokbcEEd1iLxijqtNL2BTIt4S/UYywjqh3YNymFhn1rt6jYRNzgZ/TjTtsxxXejjUKOet6tT0KPsVe+Nb2B'
                  )


btn = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(btn, GPIO.IN)

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir+'28-0214917763ea')[0]
device_file = device_folder + '/w1_slave'

def read_device_file():
    f = open(device_file,'r')
    lines = f.readlines()
    f.close()
    return lines

def parse_temperature():
    lines = read_device_file()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.1)
        lines = read_device_file('t=')
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temperature_string = lines[1][equals_pos+2:]
        temperature_c = float(temperature_string)/1000.0
        temperature_f = temperature_c * 9.0 / 5.0 + 32
        
        return temperature_c, temperature_f

try:
    print("Process start")
    while True:
        if GPIO.input(btn)==GPIO.LOW:
            print("btn pressed")
            tmp = 0
            for i in range(3):
                c, f = parse_temperature()
                print('c{:.1f}, f{:.1f}'.format(c,f))
                if c > tmp:
                    tmp = c
                time.sleep(0.3)
            response = db.get_item(TableName = "health_condition", Key={"email":{'S':'coolsuper91367@gmail.com'}})
            date = response['Item']['health']['S'].encode('utf-8')
            while date.count('/') >= 2:
                date = date.split('/')[-2]
            date = date.split(':')[0]
            string = response['Item']['temperature']['S'].encode('utf-8')
            string += date + ':' + str(round(tmp,1)) + '/'
            db.update_item(TableName = 'health_condition',Key = { "email":{'S':'coolsuper91367@gmail.com'}},
                                       UpdateExpression = 'SET temperature = :t',
                                       ExpressionAttributeValues = {':t' : {"S": str(string)}})
            print("Highest tmp {:.1f}".format(tmp))
except KeyboardInterrupt:
    print("Process shut down")
    GPIO.cleanup()