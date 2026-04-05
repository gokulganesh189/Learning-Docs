import threading
import time


def task():
    time.sleep(5)
    print("Finished task")

t = threading.Thread(target=task)
t.start()
# t.join() # using this join will make the thread code just like an AWAIT method
print("Main finished")

