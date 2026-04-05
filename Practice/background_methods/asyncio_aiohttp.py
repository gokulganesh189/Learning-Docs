import asyncio
import httpx

async def hit_api():
    async with httpx.AsyncClient() as client:
        response = await client.get("http://13.200.12.138/stats/0000002")
        return response.json()

async def get_stats():
    api_response = await hit_api()
    return {
        "message": "User created",
        "api_response": api_response
    }

print(asyncio.run(get_stats()))

async def hit_api_post():
    async with httpx.AsyncClient() as client:
        await client.post("http://13.200.12.138/shorten", json={
    "long_url": "https://www.python-httpx.org/quickstart/",
    "expires_at": "2026-02-23T18:23:02.234Z"
})

async def register():
    asyncio.create_task(hit_api_post())   # fire-and-forget
    await asyncio.sleep(3)  # keep event loop alive
    return {"message": "User created"}

asyncio.run(register())