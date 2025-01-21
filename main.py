import random
import environment
import polygon
import aiohttp
import asyncio
import time

async def get_ticker_options(ticker):
    print(f"Starting get_ticker_options task: {ticker}")

    reference_client = polygon.ReferenceClient(environment.env.POLYGON_API_KEY, True)

    await asyncio.sleep(random.randrange(9))  # Simulating a delay
    response = await reference_client.get_option_contracts(ticker)

    responses = [] + [response]
    contracts = [] + response['results']

    while "next_url" in response.keys():
        response = await reference_client.get_next_page(response)
        responses.append(response)
        contracts = contracts + response['results']

    print(f"All {ticker} get_ticker_options pages received. Total pages: {len(responses)}. Total contracts: {len(contracts)}.")

    return responses
async def main():
    environment.env.load()
    tickers = [
        'FUBO',
        'AAPL',
        'ACHR',
        'TEM',
        'LUNR',
        'INTC'
    ]

    tasks = []
    for ticker in tickers:
      tasks.append(get_ticker_options(ticker))
    
    await asyncio.gather(*tasks)
    # async with aiohttp.ClientSession() as session:
    #     tasks = [fetch_data(session, url) for url in urls]
    #     results = await asyncio.gather(*tasks)
        
    #     for result in results:
    #         print(result)

if __name__ == '__main__':
    start_time = time.time()
    asyncio.run(main())
    print(f"Total time taken: {time.time() - start_time} seconds")