from time import sleep
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
motor_pin = 17
GPIO.setup(motor_pin, GPIO.OUT)

led1_pin = 27
GPIO.setup(led1_pin,GPIO.OUT)

try:
    for i in range(2):
        GPIO.output(motor_pin, GPIO.HIGH)
        sleep(2)
        GPIO.output(motor_pin, GPIO.LOW)
        sleep(2)
except:
    GPIO.cleanup()
finally:
    GPIO.cleanup()