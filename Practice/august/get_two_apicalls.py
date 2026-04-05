import asyncio
import aiohttp

# calling each api call asynchronously
async def fetch_data(session, url):
    async with session.get(url) as response:
        return await response.json()                    
    
# calling two api calls asynchronously
async def get_two_apicalls(url1, url2):
    async with aiohttp.ClientSession() as session:
        task1 = asyncio.create_task(fetch_data(session, url1))
        task2 = asyncio.create_task(fetch_data(session, url2))
        
        response1 = await task1
        response2 = await task2
        
        return response1, response2