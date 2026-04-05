from multiprocessing import Process
import os


def task():
    print("PID:", os.getpid())
    print("Hello from child process")
    

def other_task():
    print("PID:", os.getpid())
    print("Hello from other child process")

if __name__ == "__main__":
    p = Process(target=task)
    q = Process(target=other_task)
    p.start()
    q.start()
    p.join()
    q.join()