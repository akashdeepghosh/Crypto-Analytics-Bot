# Moralis API wrapper

# References
# API Docs: https://docs.moralis.io/moralis-dapp/web3-sdk/nft-api

import os, logging
from typing import List, Dict
from httpx_client import s


API_KEY = os.environ['MORALIS_KEY']


def get_nft_owners(address: str, token_id: int) -> List[Dict]:
  """Returns the list of owners of the NFT with the given token ID"""

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

  # Returns the json dictionary
  return response.json()

def get_nfts(owner: str) -> List[Dict]:
  """Returns the list of NFTs owned by the given address"""

  url = f"https://api.moralis.io/v2/nft/owners/{owner}"
  
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

    # Returns the json dictionary
    return response.json()


def search_nfts(query: str) -> List[Dict]:
  """Returns the list of NFTs matching the given query"""

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

  # Returns the json dictionary
  return response.json()


def get_nft_lowest_price(address: str) -> List[Dict]:
  """Returns the lowest price of the NFTs owned by the given address"""

  url = f"https://api.moralis.io/v2/nft/lowest-price/{address}"
  
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

  # Returns the json dictionary
  return response.json()


def token_id_metadata(address: str, token_id: int) -> Dict:
  """Returns the metadata of the NFT with the given token ID"""

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

  # Returns the json dictionary
  return response.json()


def get_wallet_token_id_transfers(address: str, token_id: int) -> List[Dict]:
  """Returns the list of transfers of the NFT with the given token ID"""
  
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

  # Returns the json dictionary
  return response.json()
