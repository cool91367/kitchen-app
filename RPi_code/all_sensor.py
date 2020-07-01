#! /usr/bin/python2
# coding: utf8
import time
from time import sleep
import RPi.GPIO as GPIO
import sys
import os
from bluetooth import *
import uuid
from datetime import datetime
 
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
 
import Adafruit_SSD1306

import Adafruit_GPIO.SPI as SPI
import MAX6675.MAX6675 as MAX6675


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

##########led##########
led1_pin = 27
GPIO.setup(led1_pin, GPIO.OUT)
#######################

##########motor##########
motor_pin = 17
GPIO.setup(motor_pin, GPIO.OUT)
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
count = 0
try:
    while True:
        data = client_sock.recv(1024).decode("utf-8").lower()
        if len(data) == 0:
            break
        print "received [%s]" % data
        
        if "sault" in data:   
            salt = data.split(":")[1]
            gram = salt.split("g")[0]
        
        val = max(0,int(hx.get_weight(5)))
        #val = hx.get_weight(5)
        load = os.getloadavg()
        draw.rectangle((0, 0, width, height), outline=0, fill=0)
        draw.text((0, 0), 'All:'+str(val) + 'g Need:' + gram, font=font,fill=255)
        disp.image(image)
        disp.display()
        time.sleep(0.2)
        print(val)

        hx.power_down()
        hx.power_up()
        time.sleep(0.1)
        
        #vibrate
        #count = count+1
        #if(count<10):
        GPIO.output(motor_pin, GPIO.HIGH)
        GPIO.output(led1_pin, GPIO.HIGH)
        temp = sensor.readTempC()
        sleep(2)
        GPIO.output(motor_pin, GPIO.LOW)
        GPIO.output(led1_pin, GPIO.LOW)
        print 'Thermocouple Temperature: {0:0.3F}°C / {1:0.3F}°F'.format(temp, c_to_f(temp))
            
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


