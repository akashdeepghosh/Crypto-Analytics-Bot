# Module to do data analytics on the data returned by the Etherscan API

import re
import pytz, numpy
from datetime import datetime
from typing import List, Dict
from etherscan_api import Transaction, get_normal_transactions


def get_transactions_by_month(transactions: List[Transaction], month_num: int, year_num: int, timezone: pytz.timezone) -> List[Transaction]:
  """Function to get the transactions in a specific month"""

  # The list of transactions in a given month and year
  month_transactions = []

  # Iterates the list of transactions
  for transaction in transactions:

    # Creates a datetime object from the timestamp
    date_obj = datetime.fromtimestamp(int(transaction.timeStamp))

    # Localize the time to the timezone given
    local_time = timezone.localize(date_obj, is_dst=None)

    # Checks if the month and year match the wanted month and year
    if local_time.month == month_num and local_time.year == year_num:

      # Appends the transaction to the list
      month_transactions.append(transaction)

  # Returns the list of transactions
  return month_transactions


def get_transactions_by_past_months(address: str, number_of_months: int, timezone: pytz.timezone) -> List[Transaction]:
  """Function to get the transactions for the past n months"""

  # Gets the list of transactions from the API
  transactions = get_normal_transactions(address)

  # Gets the local time
  local_time = timezone.localize(datetime.now(), is_dst=None)

  # Gets the current month and year
  current_month, current_year = local_time.month, local_time.year

  # Subtract the number of months from the current month
  month = current_month - number_of_months

  # Gets the starting year
  year = current_year

  # Iterates while the starting month is less than or equal to 0
  while month <= 0:

    # Add 12 to the starting month
    month += 12

    # Gets the starting year as 1 less than the current year
    year -= 1

  # The list of transactions
  transaction_list = []

  # Iterates the months
  while True:

    # Checks if the month and the year are the same as the current ones
    if month == current_month and year == current_year:

      # Breaks the loop
      break

    # Gets the transactions in the month
    month_transactions = get_transactions_by_month(transactions, month, year, timezone)

    # Adds the month transaction to the transaction list
    transaction_list += month_transactions

    # Checks if the month is 12
    if month == 12:

      # Sets the month to 1
      month = 1

      # Increase the year by 1
      year += 1

    # If the month isn't 12
    else:

      # Increase the month by 1
      month += 1

  # Returns the list of transactions
  return transaction_list


def net_for_a_month(month_transactions: List[Transaction], address: str) -> float:
  """Function to get the net gain or net loss in a given month for the wallet"""

  # The net gain or loss in Wei
  net: int = 0

  # Iterates the transactions
  for transaction in month_transactions:

    # Checks if the transaction is incoming
    if transaction.to == address:

      # Increase the net by the transaction amount
      net += int(transaction.value)

    # Checks if the address is outgoing
    elif transaction.__dict__["from"] == address:

      # Decrease the net by the transaction amount
      net -= int(transaction.value)

  # Returns the net gain or loss in Ether
  return float(net) / (10**18)


def net_for_past_months(address: str, months: int, timezone: pytz.timezone) -> Dict[int, float]:  
  """Function to get the mapping of months (maximum 6 months) to their net gain or loss"""

  # Gets the list of transactions from the API
  transactions = get_normal_transactions(address)

  # Gets the local time currently
  local_time = timezone.localize(datetime.now(), is_dst=None)

  # Gets the month and the year
  current_month, current_year = local_time.month, local_time.year

  # Subtract the number of months from the current month
  month = current_month - months

  # Gets the starting year
  year = current_year

  # Checks if the starting month is less than or equal to 0
  if month <= 0:

    # Add 12 to the starting month
    month += 12

    # Gets the starting year as 1 less than the current year
    year -= 1

  # The dictionary that maps the month number to the net gain or loss in Ether
  month_net_dict: Dict[int, float] = {}

  # Iterates the months
  while True:

    # Checks if the month and the year are the same as the current ones
    if month == current_month and year == current_year:

      # Breaks the loop
      break

    # Gets the transactions in the month
    month_transactions = get_transactions_by_month(transactions, month, year, timezone)

    # Gets the net gain or loss in the month
    month_net_dict[month] = net_for_a_month(month_transactions, address)

    # Checks if the month is 12
    if month == 12:

      # Sets the month to 1
      month = 1

      # Increase the year by 1
      year += 1

    # If the month isn't 12
    else:

      # Increase the month by 1
      month += 1

  # Returns the dictionary of the net gain or loss in Ether for each month
  return month_net_dict


class ASCIIGraph:
  """Class that represents an ascii graph"""

  # The maximum width of the graph on before the graph overflows on an iPhone 7
  MAX_WIDTH = 31

  # The maximum number of rows that can be displayed
  MAX_ROWS = 13
  
  # The dictionary that maps the month number to the short name of the month
  month_dict = {
    1 : "Jan",
    2 : "Feb",
    3 : "Mar",
    4 : "Apr",
    5 : "May",
    6 : "Jun",
    7 : "Jul",
    8 : "Aug",
    9 : "Sep",
    10 : "Oct",
    11 : "Nov",
    12 : "Dec"
  }

  # The dictionary mapping the number of months to a tuple of where the months should be positioned
  position_dict = {
    
    # Number of months: Position(s) on the graph
    1 : (14, ),
    2 : (6, 22),
    3 : (6, 14, 22),
    4 : (0, 9, 19, 28),
    5 : (0, 7, 14, 21, 28),
    6 : (1, 6, 11, 17, 22, 27)
  }

  
  def __init__(self, month_net_dict: Dict[int, float]) -> None:
    self.month_net_dict = month_net_dict
    

  def write_value_to_the_graph(self, row_list: List[List[str]], row: int, line_position: int, net: float) -> List[List[str]]:
    """Function to write the value of the net gain or net loss to the graph"""

    # Convert the net value to a string after rounding to 3 significant figures
    net_str = str(numpy.format_float_positional(net, precision=3, unique=False, fractional=False, trim="-"))

    # Replace three 0s at the end of the string with "k"
    net_str = re.sub(r"000\Z", "k", net_str)

    # Gets the length of the net value
    net_length = len(net_str)

    # Gets the center of the string
    center: int = net_length // 2

    # Checks if the length is even
    if net_length % 2 == 0:

      # Subtract 1 from the center
      center -= 1

    # Gets the start position of the net value string
    start_pos = line_position - center

    # Checks if the start position of the string is less than 0
    if start_pos < 0:

      # Set the start position to 0
      start_pos = 0

    # Checks if the end position of the string is greater than the length of the line
    elif start_pos + net_length > self.MAX_WIDTH:

      # Sets the start position to the length of the line minus the length of the string
      start_pos = self.MAX_WIDTH - net_length
      
    # Adds the net value to the line
    row_list[row][start_pos: start_pos + net_length] = net_str

    # Returns the changed row list
    return row_list
  
  
  def write_column(self, row_list: List[List[str]], line_position: int, length: int, x_axis_row: int, net: int) -> List[List[str]]:
    """Function to create the lines on the graph"""
    
    # Checks if the value is negative
    if net < 0:

      # Gets the range of rows (from the x axis row to the x axis row plus the length of the line)
      row_range = range(x_axis_row + 1, x_axis_row + 1 + length)

      # Calls the function to write the value of net to the graph
      row_list = self.write_value_to_the_graph(row_list, x_axis_row + length + 1, line_position, net)

    # If the value isn't negative
    else:

      # Gets the range of rows (from the x axis row minus the length of the line to the x axis row)
      row_range = range(x_axis_row - length, x_axis_row)

      # Calls the function to write the value of net to the graph
      row_list = self.write_value_to_the_graph(row_list, x_axis_row - length - 1, line_position, net)

    # Iterates the row range
    for i in row_range:

      # Sets the value of the line position inside each row to a pipe character
      row_list[i][line_position] = "|"

    # Returns the edited row list
    return row_list

    
  def construct(self) -> str:
    """Function to build an ascii graph with the list of months"""

    # The values in the dictionary
    values = self.month_net_dict.values()

    # Gets the length of the dictionary
    dict_length = len(values)
      
    # Highest net
    highest = max(values)
  
    # Lowest net
    lowest = min(values)
  
    # Checks if the lowest is more than zero
    if lowest >= 0:

      # Sets the lowest to 0
      lowest = 0
  
    # The list of rows
    row_list: List[List[str]] = [[" "] * self.MAX_WIDTH for i in range(self.MAX_ROWS + 1)]

    # Scale factor (how much ether for 1 pipe character)
    scale_factor: float = (highest - lowest) / (self.MAX_ROWS - 3)

    # Changes the scale factor to 1 if it's 0
    scale_factor = 1.0 if scale_factor == 0 else scale_factor

    # Checks if the lowest value is not negative
    if lowest >= 0:

      # Gets the x axis row
      x_axis_row = self.MAX_ROWS

    # The lowest value is negative
    else:

      # Gets the number of pipe characters the lowest value will take up
      num_pipe_chars: int = abs(lowest // scale_factor)

      # Gets the x axis row
      x_axis_row = -1 + num_pipe_chars

    # Change the x axis row to have "-" characters
    row_list[x_axis_row] = ["-"] * self.MAX_WIDTH

    # Gets the positions from the length of the dictionary
    positions = self.position_dict[dict_length]

    # Initialise the index variable to keep track of where the index is in the tuple
    index = 0

    # Iterates the month and net value dictionary
    for month_num, net_value in self.month_net_dict.items():

      # Gets the position of the month name on the x axis row
      line_position = positions[index]

      # Gets the month from the month dictionary
      month = self.month_dict[month_num]

      # Writes the month to the x axis row
      row_list[x_axis_row][line_position: line_position + 3] = month
      
      # Gets the length of the line on the graph
      line_length = abs(int(net_value / scale_factor))

      # Calls the write column function to write the line onto the graph
      row_list = self.write_column(row_list, line_position + 1, line_length, x_axis_row, net_value)

      # Increase the index by 1
      index += 1

    # Returns the ascii graph
    return "\n".join("".join(row) for row in row_list)


def get_graph(address:str, number_of_months: int, timezone: pytz.timezone) -> str:
  """Function to get the ascii graph for the past n months"""

  # Gets the month net dictionary
  month_net_dict = net_for_past_months(address, number_of_months, timezone)

  # Returns the ascii graph
  return ASCIIGraph(month_net_dict).construct()
  

if __name__ == "__main__":

  print(get_graph("0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae", 4, pytz.timezone("Asia/Singapore")))