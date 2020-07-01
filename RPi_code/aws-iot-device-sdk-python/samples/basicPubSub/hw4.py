from picamera import PiCamera
from time import sleep
import boto3
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging
import json

# setting s3 client
s3 = boto3.client('s3',
                  aws_access_key_id='ASIAWQUDI2Q3CWSKEM6A',
                    aws_secret_access_key= 'uLsuuDvstDk/4GpJ1GSuSVFJQtfSkap3OhrSpJFG',
                    aws_session_token= 'FwoGZXIvYXdzEIz//////////wEaDCw4Jms3rNx59IWTVSLKAXFSLmdwjHFXA10+fE3cw+bBHnK+Ckf/XIpPZ3DlAtfp5x24abPbB3lyJlOnaiifPR77ImHXOPLcU8fY5m/D2mCnsgtpvVpIyLVpg6SisdbTs1hWNoH04JUEVDi8F8upUYr1ToCbB7yF71vgLggCMHiIIi3LcmiUfxRsVoRwLHQvv9xaHag+d3hrynqK8jZQu9iSyZZBNChs22jbYVWhGwj80PlcdyswS9jmf2lPIeMeN4NtrbeDb1v2iZsp47K1kx3P+VuZhCbZCgYouJq+9gUyLWUuBR4Jt0QBLvIR/U2xbZD4lPtvMNKH6pwDU7UBrN1DArmnWkXDDG49j95JLA=='
                  )
# setting iot subscription
# Custom MQTT message callback
def customCallback(client, userdata, message):
    print("Received a new message: ")
    print(message.payload)
    json_msg = json.loads(str(message.payload, 'utf-8'))
    face_detect = json_msg.message
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")
    
host = 'aifc1a3xa2vzj-ats.iot.us-east-1.amazonaws.com'
rootCAPath = '/home/pi/Desktop/root-CA.crt'
certificatePath = '/home/pi/Desktop/hw4.cert.pem'
privateKeyPath = '/home/pi/Desktop/hw4.private.key'
topic='$aws/things/hw4/shadow/update/accepted'
useWebsocket = False
clientId = 'basicPubSub'
port = 8883

# Configure logging
logger = logging.getLogger("AWSIoTPythonSDK.core")
logger.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

# Init AWSIoTMQTTClient
myAWSIoTMQTTClient = None
myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId)
myAWSIoTMQTTClient.configureEndpoint(host, port)
myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

# AWSIoTMQTTClient connection configuration
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

# Connect and subscribe to AWS IoT
myAWSIoTMQTTClient.connect()

myAWSIoTMQTTClient.subscribe(topic, 1, customCallback)

while True:
    #camera = PiCamera()

    #camera.start_preview()

    #sleep(2)

    #camera.capture('/home/pi/Desktop/image2.jpg')

    #s3.upload_file('/home/pi/Desktop/image2.jpg', 'nthu-105062172', 'test1.jpg')

    #camera.stop_preview()
    #sleep(3)
    sleep(2)


                    
