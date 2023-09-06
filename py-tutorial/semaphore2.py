# importing the modules
import threading      
import time        
  
# creating thread instance where count = 3
obj = threading.Semaphore(3)        
  
# creating instance
def display(name):    
    
    # calling acquire method
    obj.acquire()                
    for i in range(5):
        print('Hello, ', end = '')
        time.sleep(1)
        print(name)
          
        # calling release method
        obj.release()    
          
# creating multiple thread 
t1 = threading.Thread(target = display , args = ('Thread-1',))
t2 = threading.Thread(target = display , args = ('Thread-2',))
t3 = threading.Thread(target = display , args = ('Thread-3',))
t4 = threading.Thread(target = display , args = ('Thread-4',))
t5 = threading.Thread(target = display , args = ('Thread-5',))
  
# calling the threads 
t1.start()
t2.start()
t3.start()
t4.start()
t5.start()