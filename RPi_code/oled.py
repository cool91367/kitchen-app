import time
import sys
import os
from datetime import datetime
 
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
 
import Adafruit_SSD1306
 
FONT_SIZE = 20
 
 
disp = Adafruit_SSD1306.SSD1306_128_32(rst=0)
 
disp.begin()
disp.clear()
disp.display()
 
width = disp.width
height = disp.height
 
image = Image.new('1', (width, height))
draw = ImageDraw.Draw(image)
 
font=ImageFont.truetype("/home/pi/Desktop/fonts/NotoSans-Black.ttf", FONT_SIZE)
#font = ImageFont.load_default()
try:
    while True:
        load = os.getloadavg()
 
        draw.rectangle((0, 0, width, height), outline=0, fill=0)
        draw.text((0, 0), '12gfd3', font=font,fill=255)
        disp.image(image)
        disp.display()
        time.sleep(0.2)
except KeyboardInterrupt:
    print('fuck')
finally:
    disp.clear()
    disp.display()