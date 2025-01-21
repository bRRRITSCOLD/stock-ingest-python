import asyncio
import random
import polygon
import environment


class Ticker:
  ticker: str
  reference_options: list[any]

  def __init__(self, ticker: str):
    self.ticker = ticker

  async def get_reference_options(self):
    print(f"Starting get_ticker_options task: {self.ticker}")

    reference_client = polygon.ReferenceClient(environment.env.POLYGON_API_KEY, True)

    await asyncio.sleep(random.randrange(9))  # Simulating a delay
    response = await reference_client.get_option_contracts(self.ticker)

    responses = [] + [response]
    self.reference_options = [] + response['results']

    while "next_url" in response.keys():
        response = await reference_client.get_next_page(response)
        responses.append(response)
        self.reference_options = self.reference_options + response['results']

    print(f"All {self.ticker} get_ticker_options pages received. Total pages: {len(responses)}. Total contracts: {len(self.reference_options)}.")
