# Moralis API wrapper

# References
# API Docs: https://docs.moralis.io/moralis-dapp/web3-sdk/nft-api

import os, logging
from typing import List, Dict
from httpx_client import s


API_KEY = os.environ['MORALIS_KEY']


class Result:
  """Class that represents the results from the Moralis API"""

  def __init__(self, **attributes) -> None:
    self.__dict__.update(attributes)


def get_results(json_response: List[Dict[str, str]]) -> List[Result]:
  """Function to return the response as an object"""

  # Gets the results from the dictionary
  results = json_response.get("result")

  # Checks if the results is not nothing
  if results is not None:

    # Returns the list of responses
    return [Result(**result) for result in results]


def get_nft_owners(address: str, token_id: int) -> List[Result]:
  """Returns the list of owners of the NFT with the given token ID"""

  # The URL for the API
  url = f"https://api.moralis.io/v2/nft/{address}/{token_id}/owners"

  # Keep trying until the request succeeds
  while True:
    try:

      # Gets the response
      response = s.get(url, headers={"Authorization": f"Bearer {API_KEY}"})

      # Breaks the loop if successful
      break

    # Logs the error
    except Exception as e:
      logging.error(e)

  # Returns the list of results
  return get_results(response.json())

def get_nfts(address: str) -> List[Result]:
  """Returns the list of NFTs owned by the given address"""

  # The URL for the API
  url = f"https://api.moralis.io/v2/{address}/nft"
  
  # Keep trying until the request succeeds
  while True:
    try:

      # Gets the response
      response = s.get(url, headers={"Authorization": f"Bearer {API_KEY}"})
      
      # Breaks the loop if successful
      break

    # Logs the error
    except Exception as e:
      logging.error(e)

  # Returns the list of results
  return get_results(response.json())


def search_nfts(query: str) -> List[Dict]:
  """Returns the list of NFTs matching the given query"""

  # The URL for the API
  url = f"https://api.moralis.io/v2/nft/search?q={query}"
  
  # Keep trying until the request succeeds
  while True:
    try:

      # Gets the response
      response = s.get(url, headers={"Authorization": f"Bearer {API_KEY}"})
      
      # Breaks the loop if successful
      break

    # Logs the error
    except Exception as e:
      logging.error(e)

  # Returns the list of results
  return get_results(response.json())


def get_nft_lowest_price(address: str) -> List[Result]:
  """Returns the lowest price of the NFTs owned by the given address"""

  # The URL for the API
  url = f"https://api.moralis.io/v2/nft/{address}/lowestprice"
  
  # Keep trying until the request succeeds
  while True:
    try:

      # Gets the response
      response = s.get(url, headers={"Authorization": f"Bearer {API_KEY}"})
      
      # Breaks the loop if successful
      break

    # Logs the error
    except Exception as e:
      logging.error(e)

  # Returns the list of results
  return get_results(response.json())


def token_id_metadata(address: str, token_id: int) -> Result:
  """Returns the metadata of the NFT with the given token ID"""

  # The URL for the API
  url = f"https://api.moralis.io/v2/nft/{address}/{token_id}"
  
  # Keep trying until the request succeeds
  while True:
    try:

      # Gets the response
      response = s.get(url, headers={"Authorization": f"Bearer {API_KEY}"})
      
      # Breaks the loop if successful
      break

    # Logs the error
    except Exception as e:
      logging.error(e)

  # Returns the result object
  return Result(**response.json())


def get_wallet_token_id_transfers(address: str, token_id: int) -> List[Result]:
  """Returns the list of transfers of the NFT with the given token ID"""

  # The URL for the API
  url = f"https://api.moralis.io/v2/nft/{address}/{token_id}/transfers"

  # Keep trying until the request succeeds
  while True:
    try:

      # Gets the response
      response = s.get(url, headers={"Authorization": f"Bearer {API_KEY}"})

      # Breaks the loop if successful
      break

    # Logs the error
    except Exception as e:
      logging.error(e)

  # Returns the list of results
  return get_results(response.json())
