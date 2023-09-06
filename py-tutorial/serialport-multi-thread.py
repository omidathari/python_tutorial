#!/usr/bin/python

import queue
import threading
import time
import serial
import sys

exitFlag = 0

class consoleThread (threading.Thread):
   def __init__(self, threadID, name, serialport):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.serialport = serialport
   def run(self):
      print ("Console Starting " + self.name)
      console_process(self.name, self.serialport)
      print ("Console Exiting " + self.name)

def console_process(threadName : str, s : serial.Serial):
   while True:
        cmd = str(input())
        #print("cmd = ", cmd)
        if cmd == "exit":
            global exitFlag
            exitFlag = 1
            s.close()
            break
        else:
         cmd = cmd + "\n"
         if( s.is_open == True):
            try:
               print("TX = ", cmd.encode("Ascii"))
               s.write(cmd.encode("Ascii"))
            except BaseException as e:
               print(e)
               sys.exit(-1)



class serialRxThread (threading.Thread):
   def __init__(self, threadID, name, serialport : serial.Serial):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.serialport = serialport
   def run(self):
      print ("Starting " + self.name)
      process_data(self.name, self.serialport)
      print ("Exiting " + self.name)

def process_data(threadName : str, s : serial.Serial):
   while (s.is_open == True):
      try:
         res = s.readline()
         print("RX = ", res.decode().strip('\n'))
      except BaseException as e:
         print(e)
         sys.exit(-1)

threadID = 1

try:
   s = serial.Serial(sys.argv[1],baudrate=230400)

   # Create new threads
   mySerialRxThread = serialRxThread(threadID, "SerialPortRx", s)
   mySerialRxThread.start()
   threadID += 1

   myConsoleThread = consoleThread(threadID, "ConsoleProcessor", s)
   myConsoleThread.start()
   threadID += 1
except BaseException as e:
   print(e)
   sys.exit(-1)


while( exitFlag == 0):
   time.sleep(1)

print("Exiting Main Thread")