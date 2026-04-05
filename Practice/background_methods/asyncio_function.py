import asyncio

async def task():
    await asyncio.sleep(2)
    print("Finished")

async def main():
    asyncio.create_task(task())
    print("Returned immediately")
    await asyncio.sleep(3)

asyncio.run(main())