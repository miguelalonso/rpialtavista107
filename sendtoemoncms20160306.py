#!/usr/bin/python
# raspberry pi nrf24l01 hub
# more details at http://blog.riyas.org
# Credits to python port of nrf24l01, Joao Paulo Barrac & maniacbugs original c library

import RPi.GPIO as GPIO

from nrf24b import NRF24
import time
from time import gmtime, strftime

import  sys, string
import httplib
import time

domain = "localhost:85"
emoncmspath = "emoncms"
apikey = "fff23b9bb282c9e1d8e05df63745a4aa"
nodeid = 111

pipes = [[0xe8, 0xe8, 0xf0, 0xf0, 0xe1], [0xe8, 0xe8, 0xf0, 0xf0, 0xe1]]
##datos= [1231.23,1112.22,3132123.33,4123.44,5123.55]datos [1]
from array import *
##datos = array( 'f' ,[1.,2.,3.,4,5.] )
##datos  = zeros(5,Float)
datos =[1,2,3,4]
datos2=[1,2,3,4]
datos_str=["1", "2", "3","4", "5"]
csv="1,2,3,4,5"

httpServ = httplib.HTTPConnection(domain)

radio = NRF24()
radio.begin(0, 0,25,18) #set gpio 25 as CE pin
radio.setRetries(15,15)
radio.setPayloadSize(32)
####radio.setChannel(0x4c)
##radio.setDataRate(NRF24.BR_250KBPS)
radio.setPALevel(NRF24.PA_MAX)
radio.setAutoAck(1)
##radio.openReadingPipe(2,pipes[0])
radio.openReadingPipe(1,pipes[1])

radio.startListening()
radio.stopListening()

##radio.printDetails()
radio.startListening()

def sendtoemoncms(csv):
    httpServ.connect()
    time.sleep(10)
    # Send to emoncms
    httpServ.request("GET", "/"+emoncmspath+"/input/post.json?apikey="+apikey+"&node="+str(nodeid)+"&csv="+csv)
    print("GET", "/"+emoncmspath+"/input/post.json?apikey="+apikey+"&node="+str(nodeid)+"&csv="+csv)
    response = httpServ.getresponse()
    print response.read()
    time.sleep(10)
    httpServ.close()

def readdatafromNRF24():
    pipe = [1]
    while not radio.available(pipe):
        time.sleep(1000/1000000.0)
        print ("nada")
        time.sleep(10)
    recv_buffer = []
    radio.read(datos,20)
    out = ''.join(chr(i) for i in recv_buffer)
    print (datos)
    import struct
    for j in range(4):
            x=datos[(j*4):(j*4+4)]
            datos2[j]=struct.unpack('<f', struct.pack('4B', *x))[0]
    print (datos2)
    for i in range (4):
        datos_str[i]=str(datos2 [i])
    print (datos_str)
    csv=','.join(datos_str)
    print (csv)
    return csv

## una ves definidas las funciones ejecutamos el bucle loop
tinicio=time.time()
try:
    while True:
        elapsedtime=time.time()- tinicio
        csv=readdatafromNRF24()
        if elapsedtime>20:
##            print("Enviando a emoncms, time ", time.time())
            sendtoemoncms(csv)
            tinicio=time.time()
    GPIO.cleanup()
except KeyboardInterrupt:
    GPIO.cleanup()
 
