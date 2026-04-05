import asyncio
from concurrent.futures import ThreadPoolExecutor
import time

def blocking_task():
    time.sleep(2)
    return "Done"

async def main():
    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor() as pool:
        print(2+3)
        result = await loop.run_in_executor(pool, blocking_task)
        print(result)

asyncio.run(main())