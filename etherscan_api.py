# Module that wraps the Etherscan API

import os, logging
import pytz
from datetime import datetime
from typing import List, Dict, Optional
from httpx_client import s

# Get the Etherscan API key
API_KEY = os.environ["ETHERSCAN_KEY"]


class Transaction:
  """Class to represent a transaction on the ethereum blockchain"""

  def __init__(self, **attributes) -> None:
    self.__dict__.update(attributes)

  def __str__(self) -> str:
    attr_list = [f"{attr}: {value}" for attr, value in self.__dict__.items()]
    return "\n".join(attr_list)

  def read(self, timezone: pytz.timezone, hash_given: bool) -> str:
    """Function to give the most important details about a transaction"""

    # Get the most important details of the transaction into one string")}"
    details = f"Transaction {self.hash if not hash_given else ''}\nTime: {timezone.localize(datetime.fromtimestamp(int(self.timeStamp))).strftime('%d/%m/%Y, %-I:%M %p')} \nValue: {self.value} \nFrom: {self.__dict__['from']} \nTo: {self.to}"

    # Return the details
    return details


def convert_eth_to_usd(eth: float) -> float:
  """Function to convert Ether to USD"""

  # Keep trying until the request succeeds
  while True:
    try:

      # Gets the response
      response = s.get("https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd")

      # Gets the json from the response
      json_response = response.json()

      # Breaks the loop if successful
      break

    # Logs the error
    except Exception as e:
      logging.error(e)

  # Get conversion rate
  conversion_rate = float(json_response["ethereum"]["usd"])

  # Returns the amount in USD
  return float(eth) * conversion_rate

def convert_usd_to_eth(usd: float) -> float:
  """Function to convert USD to Ether"""

  # Keep trying until the request succeeds
  while True:
    try:

      # Gets the response
      response = s.get("https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd")

      # Gets the json from the response
      json_response = response.json()

      # Breaks the loop if successful
      break

    # Logs the error
    except Exception as e:
      logging.error(e)

  # Get conversion rate
  conversion_rate = float(json_response["ethereum"]["usd"])

  # Returns the amount in ETH
  return float(usd) / conversion_rate


def get_ether_balance(address: str) -> float:
  """Function to get the ether balance of an ethereum wallet"""

  # The URL for the API
  request_str = "https://api.etherscan.io/api" \
   "?module=account" \
   "&action=balance" \
   f"&address={address}" \
   "&tag=latest" \
   f"&apikey={API_KEY}"

  # Keep trying until the request succeeds
  while True:
    try:

        # Gets the response
        response = s.get(request_str)
      
        # Gets the json from the response
        json_response = response.json()
      
        # Breaks the loop if it's successful
        break

    # Logs the error
    except Exception as e:
      logging.error(e)

  # Gets the balance from the dictionary
  balance = json_response.get("result")

  # Checks if the balance is not None
  if balance is not None:
    
    # Returns the balance in Ether
    return float(balance) / (10**18)


def get_results(json_response: List[Dict[str, str]]) -> List[Transaction]:
  """Function to get the result from the json response"""

  # Gets the results from the dictionary
  results = json_response.get("result")

  # Check if the result is None
  if results is None:

    # Exits the function
    return

  # Change the list of dictionaries into a list of transaction objects and returns the list
  return [Transaction(**result) for result in results]


def get_normal_transactions(address: str, number_of_results: Optional[int] = 100) -> List[Transaction]:
  """Function to get the transactions from a ethereum wallet"""

  # The URL for the API
  request_str = "https://api.etherscan.io/api" \
   "?module=account" \
   "&action=txlist" \
   f"&address={address}" \
   "&startblock=0" \
   "&endblock=99999999" \
   "&page=1" \
   f"&offset={number_of_results}" \
   "&sort=desc" \
   f"&apikey={API_KEY}"

  # Keep trying until the request succeeds
  while True:
    try:

        # Gets the response
        response = s.get(request_str)

        # Gets the json from the response
        json_response = response.json()

        # Breaks the loop if it's successful
        break

    # Logs the error
    except Exception as e:
      logging.error(e)

  # Returns the results from the response
  return get_results(json_response)


def get_token_transactions(address: str, contract_address: bool, nft: bool, number_of_results: Optional[int] = 100) -> List[Transaction]:
  """Function to get the token (ERC-20 or NFT) transactions by a wallet"""

  # The URL for the API
  request_str = "https://api.etherscan.io/api" \
   "?module=account" \
   "&page=1" \
   f"&offset={number_of_results}" \
   "&startblock=0" \
   "&endblock=27025780" \
   "&sort=desc" \
   f"&apikey={API_KEY}" \

  # Checks if the token type is NFT
  if nft:

    # Adds the NFT action to the string
    request_str += "&action=tokennfttx"

  # The token is not an NFT
  else:
    
    # Adds the normal token action to the string
    request_str += "&action=tokentx"

  # Checks if the address is a contract address
  if contract_address:

    # Adds the contract address query to the request URL
    request_str = f"&contractaddress={address}"

  # The address is a normal address
  else:
    
    # Adds the address query to the request URL
    request_str += f"&address={address}"

  # Keep trying until the request succeeds
  while True:
    try:

      # Gets the response from the API
      response = s.get(request_str)

      # Gets the json from the response
      json_response = response.json()

      # Breaks the loop if it's successful
      break

    # Logs the error
    except Exception as e:
      logging.error(e)

  # Return the results from the request
  return get_results(json_response)
   

def get_transactions(address: str, contract_address: bool, number_of_results: Optional[int] = 100) -> List[Transaction]:
  """Function to get the transactions by a wallet"""

  # Gets the normal transactions
  normal_transactions = get_normal_transactions(address, number_of_results)

  # Gets the NFT transactions
  nft_transactions = get_token_transactions(address, contract_address, True, number_of_results)

  # Returns the combined list of transactions
  return normal_transactions + nft_transactions


def get_transaction_details(tx_hash: str) -> Transaction:
  """Function to get the details of a transaction"""

  # The URL for the API
  request_str = "https://api.etherscan.io/api" \
   "?module=proxy" \
   "&action=eth_getTransactionByHash" \
   f"&txhash={tx_hash}" \
   f"&apikey={API_KEY}"

  # Keep trying until the request succeeds
  while True:
    try:

      # Gets the response from the API
      response = s.get(request_str)

      # Gets the json from the response
      json_response = response.json()

      # Breaks the loop if it's successful
      break

    # Logs the error
    except Exception as e:
      logging.error(e)

  # Returns the transaction object
  return get_results(json_response)


def get_transaction_receipt(tx_hash: str) -> List[Transaction]:
  """Function to get the receipt of a transaction"""

  # The URL for the API
  request_str = "https://api.etherscan.io/api" \
   "?module=proxy" \
   "&action=eth_getTransactionReceipt" \
   f"&txhash={tx_hash}" \
   f"&apikey={API_KEY}"

  # Keep trying until the request succeeds
  while True:
    try:

      # Gets the response from the API
      response = s.get(request_str)

      # Gets the json from the response
      json_response = response.json()

      # Breaks the loop if it's successful
      break

    # Logs the error
    except Exception as e:
      logging.error(e)

  # Gets the result from the response
  result = json_response.get("result")

  # Checks if the result is not None
  if result is not None:

    # Returns the transaction json
    return result

if __name__ == "__main__":
  get_normal_transactions("0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae")