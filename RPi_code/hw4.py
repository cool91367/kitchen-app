#from picamera import PiCamera
from time import sleep
import RPi.GPIO as GPIO
#import boto3


#s3 = boto3.client('s3',
#                  aws_access_key_id='ASIAWQUDI2Q3CWSKEM6A',
#                    aws_secret_access_key= 'uLsuuDvstDk/4GpJ1GSuSVFJQtfSkap3OhrSpJFG',
#                    aws_session_token= 'FwoGZXIvYXdzEIz//////////wEaDCw4Jms3rNx59IWTVSLKAXFSLmdwjHFXA10+fE3cw+bBHnK+Ckf/XIpPZ3DlAtfp5x24abPbB3lyJlOnaiifPR77ImHXOPLcU8fY5m/D2mCnsgtpvVpIyLVpg6SisdbTs1hWNoH04JUEVDi8F8upUYr1ToCbB7yF71vgLggCMHiIIi3LcmiUfxRsVoRwLHQvv9xaHag+d3hrynqK8jZQu9iSyZZBNChs22jbYVWhGwj80PlcdyswS9jmf2lPIeMeN4NtrbeDb1v2iZsp47K1kx3P+VuZhCbZCgYouJq+9gUyLWUuBR4Jt0QBLvIR/U2xbZD4lPtvMNKH6pwDU7UBrN1DArmnWkXDDG49j95JLA=='
#                  )
def blink(pin):
    GPIO.output(pin, GPIO.HIGH)
    sleep(2)
    GPIO.output(pin, GPIO.LOW)
    sleep(2)
    print("fuck")
    

GPIO.setmode(GPIO.BCM)

GPIO.setup(17, GPIO.OUT)

for i in range(10):
    blink(17)
GPIO.cleanup()
#camera = PiCamera()

#camera.start_preview()

#sleep(2)

#camera.capture('/home/pi/Desktop/image2.jpg')

#s3.upload_file('/home/pi/Desktop/image2.jpg', 'nthu-105062172', 'test1.jpg')

#camera.stop_preview()