#receiving debug messages from CRM
import serial
import logging

s = serial.Serial(port='COM3',baudrate=230400)
while (s.is_open == True):
    try:
        res = s.readline()
        print(res.decode().strip('\n'))
    except BaseException as e:
        print("exception: ",e.__str__())
        logging.error(e)
        break