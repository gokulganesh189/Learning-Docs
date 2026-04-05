from concurrent.futures import ThreadPoolExecutor
import time

def task(n):
    time.sleep(2)
    return f"Task {n} done"

with ThreadPoolExecutor(max_workers=3) as executor:
    futures = [executor.submit(task, i) for i in range(5)]
    
    for future in futures:
        print(future.result())