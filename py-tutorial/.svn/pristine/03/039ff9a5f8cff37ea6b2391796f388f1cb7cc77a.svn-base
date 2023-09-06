#!/usr/bin/python

import threading

exitFlag = 0

class consoleObject:
   def __init__(self,name, input_callback):
      self.name = name
      self.input_thread = threading.Thread(target=self.console_process)
      self.input_callback = input_callback
   def start(self):
      self.input_thread.start()

   def console_process(self):
      while True:
         cmd = str(input())
         self.input_callback(cmd)


def console_input( data ):
   print("Console Input: " , data)
   if data == "exit":
      exit(-1)
   else:
      pass

consoleThread = consoleObject("ConsoleProcessor",console_input)
consoleThread.start()

# while True:
#    time.sleep(1)
