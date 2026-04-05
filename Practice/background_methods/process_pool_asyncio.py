import asyncio
from concurrent.futures import ProcessPoolExecutor
import math


def cpu_task():
    return sum(math.sqrt(i) for i in range(10_000_000))


async def main():
    loop = asyncio.get_running_loop()
    with ProcessPoolExecutor() as pool:
        result = await loop.run_in_executor(pool, cpu_task)
        print(result)


if __name__ == "__main__":
    asyncio.run(main())