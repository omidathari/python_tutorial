import threading
import queue
import time

q = queue.Queue()

def worker():
    while True:
        item = q.get()
        print(f'Working on {item}')
        #time.sleep(0.2)
        print(f'Finished {item}')
        q.task_done()

# Turn-on the worker thread.
t = threading.Thread(target=worker, daemon=True)


# Send thirty task requests to the worker.
for item in range(30):
    q.put(item)
t.start()

# Block until all tasks are done.
q.join()

time.sleep(3)
# Add more stuff into the q
for item in range(10):
    q.put(item)

val = 0
while True:
    q.put(val)
    val += 1
    time.sleep(1)

print('All work completed')