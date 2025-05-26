import asyncio
from fastmcp import Client

client = Client("core.py")

async def call_tool(name: str):
    async with client:
        # result = await client.call_tool("add", {'a': 1, 'b': 2})
        print('test')
        result = await client.call_tool("market_summary", {"symbols":["EBAY"]})

        print(result)

asyncio.run(call_tool("EBAY"))