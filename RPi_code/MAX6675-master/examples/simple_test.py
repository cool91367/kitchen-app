#!/usr/bin/python
# coding: utf8
import time
import Adafruit_GPIO.SPI as SPI
import MAX6675.MAX6675 as MAX6675

# Define a function to convert celsius to fahrenheit.
def c_to_f(c):
        return c * 9.0 / 5.0 + 32.0

# Raspberry Pi software SPI configuration.
CLK = 11
# CS  = 24
# DO  = 9
CS  = 26
DO  = 9
sensor = MAX6675.MAX6675(CLK, CS, DO)

# Loop printing measurements every second.
print 'Press Ctrl-C to quit.'
while True:
	temp = sensor.readTempC()
	print 'Thermocouple Temperature: {0:0.3F}°C / {1:0.3F}°F'.format(temp, c_to_f(temp))
	time.sleep(1.0)