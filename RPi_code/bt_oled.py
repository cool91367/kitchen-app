import os
import sys
import Adafruit_SSD1306
import glob
import time
import RPi.GPIO as GPIO
from bluetooth import *
import uuid
import sys
import os
from datetime import datetime

 
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
 

def draw_text(text,width,height):
    try:
        load = os.getloadavg()
        w,h = draw.textsize(text)
        draw.rectangle((0, 0, width, height), outline=0, fill=0)
        draw.text(((width-w)/2, (height-h)/2), text, font=font,fill=255)
        disp.image(image)
        disp.display()
        time.sleep(0.2)
    except KeyboardInterrupt:
        print('fuck')
    finally:
        disp.display()

##############################
###########OLED###############
disp = Adafruit_SSD1306.SSD1306_128_32(rst=0)
 
disp.begin()
disp.clear()
disp.display()
 
width = disp.width
height = disp.height
 
image = Image.new('1', (width, height))
draw = ImageDraw.Draw(image)

FONT_SIZE = 15
font=ImageFont.truetype("/home/pi/Desktop/fonts/NotoSans-Black.ttf", FONT_SIZE)
##############################
os.system('modprobe w1-gpio')

GPIO.setmode(GPIO.BCM)

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
while True:   
    try:
            disp.clear()
            data = client_sock.recv(1024).decode("utf-8").lower()
            if len(data) == 0:
                break
            draw_text(data,width,height)
            print "received [%s]" % data

            print "sending [%s]" % data

    except IOError:
        pass

    except KeyboardInterrupt:

        print "disconnected"

        client_sock.close()
        server_sock.close()
        print "all done"

        break

