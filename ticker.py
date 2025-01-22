import asyncio
import random
import polygon
import environment
from log import log
from utils.array import chunk


class Ticker:
  ticker: str

  option_contracts_references: list[any]
  option_contracts: list[any]

  reference_client: polygon.reference_apis.reference_api.AsyncReferenceClient
  options_client: polygon.options.options.AsyncOptionsClient

  def __init__(self, ticker: str):
    self.ticker = ticker

    self.reference_client = polygon.ReferenceClient(environment.env.POLYGON_API_KEY, True)
    self.options_client = polygon.OptionsClient(environment.env.POLYGON_API_KEY, True)

  async def get_option_contracts_references(self):
    log.debug(f"#get_option_contracts_references - ticker: {self.ticker} - beginning")


    response = await self.reference_client.get_option_contracts(self.ticker)

    responses = [] + [response]

    self.option_contracts = [] + response['results']

    while "next_url" in response.keys():
        response = await self.reference_client.get_next_page(response)
        responses.append(response)
        self.option_contracts = self.option_contracts + response['results']

    log.debug(f"#get_option_contracts_references - ticker: {self.ticker} - total pages: {len(responses)} - total contracts: {len(self.option_contracts)} - finished")
  
  async def get_option_contracts_previous_close(self):
    log.debug(f"#get_option_contracts_previous_close - ticker: {self.ticker} - total contracts: {len(self.option_contracts)} - beginning")

    async def task(ticker: str):
        response = await self.options_client.get_previous_close(ticker=ticker)
        return response

    chunked = chunk(self.option_contracts, 5)

    for batch in chunked:
      tasks = []
      for ref in batch:
        tasks.append(task(ref['ticker']))
  
      await asyncio.gather(*tasks)
    
    log.debug(f"#get_option_contracts_previous_close - ticker: {self.ticker} - total contracts: {len(self.option_contracts)} - finished")
     
