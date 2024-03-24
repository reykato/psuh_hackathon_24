from lcd1602 import LCD
import utime
from machine import Pin

import network
import rp2
import binascii
from time import sleep
import socket
import gc
gc.collect()

rp2.country('US')

ssid = 'Lindsay'
password = 'roommates'

def connect():
    #Connect to WLAN
    ap = network.WLAN(network.AP_IF)
    ap.config(essid=ssid, password=password)
    ap.active(True)
    while ap.active() == False:
        pass
    print('Connection successful')
    print(ap.ifconfig())
    
    
def startSocket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', 80))
    sock.listen(5)
    conn, addr = sock.accept()
    print('Got a connection from %s' % str(addr))
    #sock.send(b"hello")
    return conn
    #sock.close()
    
msg = ""
def listen(conn):
    global msg
    key=scanKeypad()
    if key is not None:
        if key == '#':
            if msg != "":
                lcd.clear()
                lcd.message("Sent: ")
                lcd.message(msg)
                lcd.message("\nPress # to reset")
                conn.send(bytes(msg, 'utf-8'))
                msg = ""
            else:
                lcd.clear()
                lcd.message("Message: ")
        else:
            lcd.message(key)
            msg = msg + key


lcd = LCD()

keyMatrix = [
    [ "1",    "2",   "3",    "A" ],
    [ "4",    "5",   "6",   "B"],
    [ "7",    "8",   "9",   "C" ],
    ["*",  "0", "#", "D" ]
]
colPins = [11,10, 9, 8]
rowPins = [15,14,13,12]

row = []
column = []

for item in rowPins:
    row.append(machine.Pin(item,machine.Pin.OUT))
for item in colPins:
    column.append(machine.Pin(item,machine.Pin.IN,machine.Pin.PULL_DOWN))
key = '0'
def scanKeypad():
    global key
    for rowKey in range(4):
        row[rowKey].value(1)
        for colKey in range(4):
            if column[colKey].value() == 1:
                key = keyMatrix[rowKey][colKey]
                row[rowKey].value(0)
                return(key)
        row[rowKey].value(0)
def printKey():
    key=scanKeypad()
    if key is not None:
        lcd.message(key)
    utime.sleep(0.2)
    
lcd.message("Connecting...")
connect()
deez = startSocket()
lcd.clear()
lcd.message("Message: ")
while True:
    #printKey()
    listen(deez)
    utime.sleep(0.2)
