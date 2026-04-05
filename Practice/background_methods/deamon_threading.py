import threading
import time

def task():
    time.sleep(5)
    print("Finished")

t = threading.Thread(target=task, daemon=True)
time.sleep(7)
t.start()

print("Main exits")

# example hearbeat sender when the program stops no need to do other tasks
"""When not to use deamon threads
❌ Database writes
❌ File saving
❌ Payment processing
❌ Sending critical emails
❌ Chat message persistence
"""
