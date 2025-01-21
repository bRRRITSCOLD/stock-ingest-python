import random
import environment
import polygon
import aiohttp
import asyncio
import time

from ticker import Ticker

async def get_data(ticker):
    t = Ticker(ticker)

    await t.get_reference_options()

async def main():
    environment.env.load()

    tickers = [
        'FUBO',
        'ACHR',
        'TEM',
        'LUNR',
    ]

    tasks = []

    for ticker in tickers:
      tasks.append(get_data(ticker))
    
    await asyncio.gather(*tasks)

if __name__ == '__main__':
    start_time = time.time()
    asyncio.run(main())
    print(f"Total time taken: {time.time() - start_time} seconds")