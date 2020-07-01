#! /usr/bin/python2

import time
from time import sleep
import RPi.GPIO as GPIO
import sys
import os
from datetime import datetime
 
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
 
import Adafruit_SSD1306

GPIO.setmode(GPIO.BCM)

led1_pin = 27
GPIO.setup(led1_pin, GPIO.OUT)

motor_pin = 17
GPIO.setup(motor_pin, GPIO.OUT)

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

# I've found out that, for some reason, the order of the bytes is not always the same between versions of python, numpy and the hx711 itself.
# Still need to figure out why does it change.
# If you're experiencing super random values, change these values to MSB or LSB until to get more stable values.
# There is some code below to debug and log the order of the bits and the bytes.
# The first parameter is the order in which the bytes are used to build the "long" value.
# The second paramter is the order of the bits inside each byte.
# According to the HX711 Datasheet, the second parameter is MSB so you shouldn't need to modify it.
hx.set_reading_format("MSB", "MSB")

# HOW TO CALCULATE THE REFFERENCE UNIT
# To set the reference unit to 1. Put 1kg on your sensor or anything you have and know exactly how much it weights.
# In this case, 92 is 1 gram because, with 1 as a reference unit I got numbers near 0 without any weight
# and I got numbers around 184000 when I added 2kg. So, according to the rule of thirds:
# If 2000 grams is 184000 then 1000 grams is 184000 / 2000 = 92.
#hx.set_reference_unit(113)
hx.set_reference_unit(referenceUnit)

hx.reset()

hx.tare()

print("Tare done! Add weight now...")

# to use both channels, you'll need to tare them both
#hx.tare_A()
#hx.tare_B()
count = 0
try:
    while True:
        val = max(0,int(hx.get_weight(5)))
        #val = hx.get_weight(5)
        load = os.getloadavg()
        draw.rectangle((0, 0, width, height), outline=0, fill=0)
        draw.text((0, 0), 'All:'+str(val)+'g Need: 50g', font=font,fill=255)
        disp.image(image)
        disp.display()
        time.sleep(0.2)
        print(val)

        # To get weight from both channels (if you have load cells hooked up 
        # to both channel A and B), do something like this
        #val_A = hx.get_weight_A(5)
        #val_B = hx.get_weight_B(5)
        #print "A: %s  B: %s" % ( val_A, val_B )

        hx.power_down()
        hx.power_up()
        time.sleep(0.1)
        
        #vibrate
        #count = count+1
        #if(count<10):
        GPIO.output(motor_pin, GPIO.HIGH)
        GPIO.output(led1_pin, GPIO.HIGH)
        sleep(2)
        GPIO.output(motor_pin, GPIO.LOW)
        GPIO.output(led1_pin, GPIO.LOW)
            
except (KeyboardInterrupt, SystemExit):
    cleanAndExit()
    disp.clear()
    disp.display()
    GPIO.cleanup()
finally:
    disp.clear()
    disp.display()
    cleanAndExit()
    GPIO.cleanup()

