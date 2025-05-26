import asyncio
from fastmcp import Client
import json
from pprint import pprint
symbols = ["EBAY", "MSFT"]
client = Client("core.py")

async def call_tool(names: list[str]):
    async with client:
        result = await client.call_tool("market_summary", {"symbols": names})
        text_context = result[0]
        # Pretty print the results for each symbol
        pprint(json.loads(text_context.text))
asyncio.run(call_tool(symbols))