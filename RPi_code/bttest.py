import os
import glob
import time
import RPi.GPIO as GPIO
from bluetooth import *
import uuid

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
            data = client_sock.recv(1024).decode("utf-8").lower()
            if len(data) == 0:
                break
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