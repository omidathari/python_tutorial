#!/usr/bin/python

# This module shows how to use a thread object.
# Usage
# Start the program and type anything in the console.  One of the threads will get the message
# and process it.  Type exit to exit the program.

import queue
import threading
import time

exitFlag = 0

class myConsoleThread (threading.Thread):
   def __init__(self, threadID, name, q, l):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.q = q
      self.l = l
   def run(self):
      print ("Console Starting " + self.name)
      console_process(self.name, self.q, self.l)
      print ("Console Exiting " + self.name)

def console_process(threadName : str, q : queue.Queue, l : threading.Lock):
   while True:
        cmd = str(input())
        print("cmd = ", cmd)
        if cmd == "exit":
            global exitFlag
            exitFlag = 1
            time.sleep(1)
            break
        else:
         l.acquire()
         q.put(cmd)
         l.release()

class myThread (threading.Thread):
   def __init__(self, threadID, name, q, l):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.q = q
      self.l = l
   def run(self):
      print ("Starting " + self.name)
      process_data(self.name, self.q,self.l)
      print ("Exiting " + self.name)

def process_data(threadName : str, q : queue.Queue, l : threading.Lock):
   while True:
        l.acquire()
        if not q.empty():
            data = q.get()
            l.release()
            print ("%s processing %s" % (threadName, data))
        else:
            l.release()
            #print ("%s processing none. Flag = %d." % (threadName,exitFlag))
        if(exitFlag == 1):
            break
        time.sleep(1)

threadList = ["ConsumerThread-1", "ConsumerThread-2", "ConsumerThread-3"]
queueLock = threading.Lock()
workQueue = queue.Queue(10)
threads = []
threadID = 1

# Create new threads
for tName in threadList:
   thread = myThread(threadID, tName, workQueue,queueLock)
   thread.start()
   threads.append(thread)
   threadID += 1

consoleThread = myConsoleThread(threadID, "ConsoleProcessor",workQueue,queueLock)
consoleThread.start()
threads.append(consoleThread)
threadID += 1

# Wait for all threads to complete
for t in threads:
   t.join()

while( exitFlag == 0):
   time.sleep(1)

print("Exiting Main Thread")