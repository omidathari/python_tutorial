#!/usr/bin/python

import queue
import threading
import time

exitFlag = 0

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
   while not exitFlag:
        l.acquire()
        if not q.empty():
            data = q.get()
            l.release()
            print ("%s processing %s" % (threadName, data))
        else:
            l.release()
        time.sleep(1)

threadList = ["Thread-1", "Thread-2", "Thread-3"]
nameList = ["One", "Two", "Three", "Four", "Five"]
queueLock = threading.Lock()
workQueue = queue.Queue(10)
threads = []
threadID = 1

# Create new threads
for tName in threadList:
   thread = myThread(threadID, tName, workQueue, queueLock)
   thread.start()
   threads.append(thread)
   threadID += 1

# Fill the queue
queueLock.acquire()
for word in nameList:
   workQueue.put(word)
queueLock.release()

# Wait for queue to empty
while not workQueue.empty():
   print("waiting")
   time.sleep(0.500)
   pass

# Notify threads it's time to exit
exitFlag = 1

# Wait for all threads to complete
for t in threads:
   t.join()
print("Exiting Main Thread")