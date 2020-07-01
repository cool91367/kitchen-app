import os
import glob
import time
import RPi.GPIO as GPIO

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

                time.sleep(0.3)

except KeyboardInterrupt:
    print("Process shut down")
    GPIO.cleanup()
