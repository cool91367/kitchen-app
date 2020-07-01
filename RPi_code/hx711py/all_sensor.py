#! /usr/bin/python2
# coding: utf8
import time
from time import sleep
import RPi.GPIO as GPIO
import sys
import os
from bluetooth import *
import uuid
import requests
from datetime import datetime
 
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
 
import Adafruit_SSD1306

import Adafruit_GPIO.SPI as SPI
import MAX6675.MAX6675 as MAX6675
import math

GPIO.setmode(GPIO.BCM)
os.system('modprobe w1-gpio')
##########temp##########
def c_to_f(c):
        return c * 9.0 / 5.0 + 32.0

CLK = 11
CS  = 26
DO  = 9
sensor = MAX6675.MAX6675(CLK, CS, DO)
#######################
btn_pin = 22
GPIO.setup(btn_pin,GPIO.IN)



##########led1##########
led1_pin = 27
GPIO.setup(led1_pin, GPIO.OUT)
GPIO.output(led1_pin, GPIO.LOW)
#######################

##########led2##########
led2_pin = 25
GPIO.setup(led2_pin, GPIO.OUT)
GPIO.output(led2_pin, GPIO.LOW)
#######################

##########motor##########
motor_pin = 17
GPIO.setup(motor_pin, GPIO.OUT)
GPIO.output(motor_pin, GPIO.LOW)
#######################


FONT_SIZE = 13
EMULATE_HX711=False
referenceUnit = 426.88

disp = Adafruit_SSD1306.SSD1306_128_32(rst=0)
 
disp.begin()
disp.clear()
disp.display()
 
width = disp.width
height = disp.height
 
image = Image.new('1', (width, height))
draw = ImageDraw.Draw(image)
 
font=ImageFont.truetype("/home/pi/Desktop/fonts/NotoSans-Black.ttf", FONT_SIZE)

##############################################################
server_sock=BluetoothSocket( RFCOMM )
server_sock.bind(("",PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]
service_id = "d6bb51e3-d761-4005-970f-a7c3d974d4a7"

advertise_service(server_sock,"test",
                  service_id = service_id,
                  service_classes = [service_id,SERIAL_PORT_CLASS],
                  profiles = [SERIAL_PORT_PROFILE])

#uuid = "94f39d29-7d6d-437d-973b-
       
print "Waiting for connection on RFCOMM channel %d" % port

client_sock, address = server_sock.accept()
print "Accepted connection from ", address
###############################################################

if not EMULATE_HX711:
    import RPi.GPIO as GPIO
    from hx711 import HX711
else:
    from emulated_hx711 import HX711

def cleanAndExit():
    print("Cleaning...")

    if not EMULATE_HX711:
        GPIO.cleanup()
        
    print("Bye!")
    sys.exit()

hx = HX711(5, 6)
hx.set_reading_format("MSB", "MSB")
hx.set_reference_unit(referenceUnit)
hx.reset()
hx.tare()

print("Tare done! Add weight now...")
step = 1
flag= 0
score = 40
initial_value = 0
all_gram = 0
try:
    while True:
        if flag == 1:
            temp = sensor.readTempC()
            print 'Thermocouple Temperature: {0:0.3F}°C / {1:0.3F}°F'.format(temp, c_to_f(temp))
        
        data = client_sock.recv(1024).decode("utf-8").lower()
        if len(data) == 0:
            print("break")
            break
        else:
            GPIO.output(motor_pin, GPIO.LOW)
            GPIO.output(led1_pin, GPIO.LOW)
            GPIO.output(led2_pin,GPIO.LOW)
        if "heat" in data:
            flag = 1
        else:
            flag = 0
        print "received [%s]" % data

        if "sault" in data:   
            salt = data.split(":")[1]
            gram = salt.split("g")[0]
            sauce = "salt"
            all_gram += int(gram)
            GPIO.output(led2_pin, GPIO.HIGH)
            GPIO.output(motor_pin, GPIO.HIGH)
        elif "pepper"  in data:
            pepper = data.split(":")[1]
            gram = pepper.split("g")[0]
            sauce = "pepper"
            all_gram += int(gram)
            GPIO.output(led1_pin, GPIO.HIGH)
            GPIO.output(motor_pin, GPIO.HIGH)
        elif "soysauce"  in data:
            soysauce = data.split(":")[1]
            gram = soysauce.split("g")[0]
            sauce = "soysauce"
            all_gram += int(gram)
        
        
        val = max(0,int(hx.get_weight(5)))
        #val = hx.get_weight(5)
        load = os.getloadavg()
        draw.rectangle((0, 0, width, height), outline=0, fill=0)
        if "sault" in data or "pepper" in data or "soysauce" in data:
            draw.text((0, 0), 'All:'+str(val) + 'g '+ sauce + " :"+ str(gram), font=font,fill=255)
            
            GPIO.output(motor_pin, GPIO.HIGH)
            
        else:
            draw.text((0, 0), 'All:'+str(val) + 'g ', font=font,fill=255)
        disp.image(image)
        disp.display()
        time.sleep(0.2)
        print(val)

        hx.power_down()
        hx.power_up()
        time.sleep(0.1)
        
        
        print("current step: " + str(step))
        if step == 1:
            initial_value = val
            print("initial_value :" + str(initial_value))
        step += 1
#         elif step >= 2:
#             print("step >= 2: ")
#                 
#             print(abs(int(val)-int(gram)))
# #             if "sault" in data or "pepper" in data or "soysauce" in data:
#             
#             dif = abs(int(val)-int(pre_all))
#             if abs(int(gram) - dif) > 3 and dif > 3:
#                 score -= abs(int(gram) - dif)
#                 
#             print("current val:" + str(val))
#             print("pre val:" + str(pre_all))
#             print("current score:" + str(score))
#             pre_all = val
        print("current all_gram:" + str(all_gram))
        
        score = max(0,int(score))
        if "finish" in data:
            last_value = val
            dif = abs(int(last_value) - int(initial_value))
            print("last_value" + str(last_value))
            print("initial_value" + str(initial_value))
            print("diff :" + str(dif))
            print("all_gram :" + str(all_gram))
            if abs(int(dif)-int(all_gram)) > 3:
                score -= abs(int(dif) - int(all_gram))
            print("here")
            url = "https://c4g74e1ku1.execute-api.us-east-1.amazonaws.com/default/calaulate_score"
            myobj = {'name': 'mapo',
                     'sensorScore': str(score)}
            re = requests.post(url, data = myobj)
            print(re)    
        
except (KeyboardInterrupt, SystemExit):
    cleanAndExit()
    disp.clear()
    disp.display()
    GPIO.cleanup()
    client_sock.close()
    server_sock.close()
finally:
    disp.clear()
    disp.display()
    cleanAndExit()
    GPIO.cleanup()
    client_sock.close()
    server_sock.close()

