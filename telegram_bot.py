# The telegram bot

import os, re
import etherscan_api, data_analytics
import pytz
from typing import Union, List
from replit import db
from telebot import TeleBot
from telebot.types import Message, ReplyKeyboardMarkup, ReplyKeyboardRemove

# The telegram bot
bot = TeleBot(token=os.environ["TELEGRAM_TOKEN"])


def save_timezone_to_db(chat_id: Union[int, str], timezone: str) -> None:
  """Function to save the timezone to the database if it's not inside"""

  # The flag to signify the chat ID is in the database
  in_db = False
  
  # The list of saved timezones
  saved_tzs = db["timezones"]

  # Iterates the saved timezones in the database
  for index, saved_tz in enumerate(saved_tzs):

    # Checks if the saved timezone starts with the chat ID
    if saved_tz.startswith(str(chat_id)):

      # Edits the saved timezone
      saved_tzs[index] = f"{chat_id} {timezone}"

      # Sets the flag to True
      in_db = True

      # Breaks the loop
      break

  # Checks if the timezone is not in the database
  if not in_db:

    # Appends to the list of saved timezones
    saved_tzs.append(f"{chat_id} {timezone}")

  # Assigns the edited saved timezone list to the database one
  db["timezones"] = saved_tzs


def get_timezone_from_db(chat_id: Union[str, int]) -> pytz.timezone:
  """Function to get the timezone from the database"""

  # Gets the filtered list of the saved timezone
  saved_tz = [tz for tz in db["timezones"] if tz.startswith(str(chat_id))]

  # Checks if the list is not empty
  if saved_tz:

    # Returns the timezone
    return pytz.timezone(saved_tz[0].split()[1])

  # Returns UTC otherwise
  return pytz.timezone("UTC")


def create_timezone_keyboard(timezone_list: [pytz.all_timezones, pytz.common_timezones]) -> ReplyKeyboardMarkup:
  """Function to create the reply keyboard for timezones"""

  # Create the reply keyboard
  keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

  # Adds all the timezones in the list to the reply keyboard
  for timezone in timezone_list:
    keyboard.row(timezone)

  # Returns the keyboard
  return keyboard


def get_timezone(message: Message) -> None:
  """Function to get the timezone from the user"""

  # Gets the text from the message
  timezone = message.text

  # Checks if the timezone is not in the list of all timezones
  if timezone not in pytz.all_timezones_set:

    # Creates the invalid timezone message
    bot_msg = "Invalid timezone entered, please enter a valid timezone in the format \"Continent/Country\"."
    
    # Sends the message with the keyboard again
    bot.send_message(message.chat.id, bot_msg, reply_markup=create_timezone_keyboard(pytz.all_timezones))

    # Exits the function and call this function again after the next message
    return bot.register_next_step_handler(message, get_timezone)

  # Otherwise, save the timezone to the database
  save_timezone_to_db(message.chat.id, timezone)

  # Sends the message that the timezone has been saved
  bot.send_message(message.chat.id, f"Your timezone has been saved as {timezone}.", reply_markup=ReplyKeyboardRemove())
  

@bot.message_handler(commands=["start"])
def start_handler(message: Message) -> None:
  """Function to handle the /start command"""

  # The bot message to send to the user
  bot_msg = "Hello! This is a bot that perform data analytics on your crypto wallet. To start, please enter your timezone in the format \"Continent/Country\" or pick one of the timezones in the list. \n\nUse the /help command to get more information about how to use the bot."

  # Sends the message
  bot.send_message(message.chat.id, bot_msg, reply_markup=create_timezone_keyboard(pytz.common_timezones))

  # Register the next function
  bot.register_next_step_handler(message, get_timezone)


@bot.message_handler(commands=["help"])
def help_handler(message: Message) -> None:
  """Function to handle the /help command"""

  # Creates the help message
  help_msg = """Here is how you can use the bot's functions:

/changetimezone
-> Changes your timezone

/currenttimezone
-> Shows the current timezone the bot is set to

/ethbalance <address>
-> Gets the account balance of your ethereum wallet

/ethprice
-> Gets the current price of Ether in USD

/convert
-> Converts USD to Ether and vice versa

/gettxdetails <transaction hash>
-> Gets the details of the transaction

/gettxs <address> <number of transactions (n) (optional)>
-> Gets the past n transactions (defaults to the past 100 transactions)

/getpasttxs <address> <number of months (n) (optional)>
-> Gets the transactions for the past n months (defaults to 6 months)

/getanalytics <address> <number of months (n) (optional, maximum of 6 months)>
-> Gets the analytics graph for given number of months (defaults to the maximum of 6 months)
  """

  # Sends the help message to the user
  bot.send_message(message.chat.id, help_msg)


@bot.message_handler(commands=["changetz", "changetimezone"])
def change_timezone(message: Message) -> None:
  """Function to handle the /changetz command"""

  # Gets the message text
  msg = message.text

  # Remove the command from the message
  msg = re.sub(r"/changetz|/changetimezone", "", msg).strip()

  # Checks if the message is in the set of timezones
  if msg in pytz.all_timezones_set:

    # Save the timezone to the database
    save_timezone_to_db(message.chat.id, msg)

    # Sends a message back to say that the timezone has been saved and exits the function
    return bot.send_message(message.chat.id, f"Timezone has been changed to {msg}.")

  # Otherwise, send the message telling the user to enter a timezone
  bot.send_message(message.chat.id, "Please enter your timezone or select one from the list.", reply_markup=create_timezone_keyboard(pytz.common_timezones))

  # Register the get timezone function as the next function
  bot.register_next_step_handler(message, get_timezone)


@bot.message_handler(commands=["currenttimezone", "currenttz"])
def current_tz_handler(message: Message) -> None:
  """Function to handle the /currenttimezone command"""

  # Gets the timezone from the database
  timezone = get_timezone_from_db(message.chat.id)

  # Sends the message to the user
  bot.send_message(message.chat.id, f"The current timezone the bot is set to is {timezone.zone}.")


@bot.message_handler(commands=["ethbalance", "ethbal"])
def eth_balance(message: Message) -> None:
  """Function to handle the /ethbalance command"""
  
  # Gets the text of the message
  msg = message.text

  # Removes the command from the message
  msg = re.sub("/ethbalance|/ethbal", "", msg).strip()

  # Checks if the message has an address behind
  if msg:

    # Calls the etherscan API to get the balance of the address
    balance = etherscan_api.get_ether_balance(msg)

    # Sends the balance back to the user and exit the function
    return bot.send_message(message.chat.id, f"Your ethereum wallet balance is {balance} ETH.")

  # Sends the message to ask the user to input their address
  bot.send_message(message.chat.id, "Please input your ethereum wallet address.")

  # Register this function as the next step handler
  bot.register_next_step_handler(message, eth_balance)


@bot.message_handler(commands=["ethprice"])
def get_ether_price(message: Message) -> None:
  """Function to handle the /ethprice command to get the price of Ether in USD"""

  # Returns the ethereum price from the API
  bot_msg = str(etherscan_api.convert_eth_to_usd(1))

  # Sends the message to the user
  bot.send_message(message.chat.id, bot_msg)


@bot.message_handler(commands=["convert"])
def handle_convert(message: Message) -> None:
  """Function to handle the /convert command"""

  # Creates the reply keyboard
  keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

  # Adds the two options to the keyboard
  keyboard.row("ETH to USD").row("USD to ETH")

  # Sends the message to the user
  bot.send_message(message.chat.id, "Please pick one of the conversions.", reply_markup=keyboard)

  # Register the next function
  bot.register_next_step_handler(message, ask_for_amount)


def ask_for_amount(message: Message) -> None:
  """Function to ask for the amount"""

  # Gets the text from the message
  msg = message.text

  # Checks if the message given is not in the 2 options
  if msg not in {"ETH to USD", "USD to ETH"}:

      # Creates the reply keyboard
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
  
    # Adds the two options to the keyboard
    keyboard.row("ETH to USD").row("USD to ETH")

    # Sends a message to the user telling them that it is invalid
    bot.send_message(message.chat.id, "Invalid option, please pick again.", reply_markup=keyboard)

    # Registers this function as the next step handler and exit the function
    return bot.register_next_step_handler(message, ask_for_amount)

  # Sends a message to the user to enter their amount requested
  bot.send_message(message.chat.id, "Please enter the amount you want to convert.", reply_markup=ReplyKeyboardRemove())

  # Register the next function
  bot.register_next_step_handler(message, convert, msg)


def convert(message: Message, type: str) -> None:
  """Function to convert the amount given"""

  # Gets the text from the message
  msg = message.text

  # Checks if the message is not a number
  if not re.search(r"^\d+$|^\d+\.\d+$", msg):

    # Sends an invalid input message to the user
    bot.send_message(message.chat.id, "Invalid amount given, please enter another amount.")

    # Registers this function as the next step handler and exits the function
    return bot.register_next_step_handler(message, convert, type)

  # Checks if the type is ETH to USD
  if type == "ETH to USD":

    # Calls the API to get the converted amount
    converted_amt = etherscan_api.convert_eth_to_usd(float(msg))

    # The unit for the conversion
    unit = "USD"

  # Checks if the type is USD to ETH
  elif type == "USD to ETH":

    # Calls the API to get the converted amount
    converted_amt = etherscan_api.convert_usd_to_eth(float(msg))

    # The unit for the conversion
    unit = "ETH"
    
  # Sends the message to the user
  bot.send_message(message.chat.id, f"The converted amount is {converted_amt} {unit}.")


@bot.message_handler(commands=["gettxdetails", "gettxdeets"])
def transaction_details_handler(message: Message) -> None:
  """Function to handle the /gettxdetails command"""

  # Gets the text from the message
  msg = message.text

  # Removes the command
  msg = re.sub("/gettxdetails|/gettxdeets", "", msg).strip()

  # Checks if the message is not empty
  if msg:

    # Calls the API to get the transaction object
    transaction = etherscan_api.get_transaction_details(msg)

    # Gets the details of the transaction
    details = transaction.read(get_timezone_from_db(message.chat.id), True)

    # Sends the message to the user and exits the function
    return bot.send_message(message.chat.id, details)

  # Otherwise, sends a message to the user to input their transaction hash
  bot.send_message(message.chat.id, "Please enter your transaction hash.")

  # Registers this function as the next step handler
  bot.register_next_step_handler(message, transaction_details_handler)


@bot.message_handler(commands=["gettxs", "gettx"])
def get_transactions_handler(message: Message) -> None:
  """Function to handle the /gettxs command"""

  # Gets the text from the message
  msg = message.text

  # Removes the command
  msg = re.sub("/gettxs|/gettx", "", msg).strip()

  # Checks if the message is not empty
  if msg:

    # Gets the list of words in the message
    msg_list = msg.split()

    # Checks if the length of the list is 1
    if len(msg_list) == 1:

      # Calls the API to get the list of transactions
      transactions = etherscan_api.get_normal_transactions(msg)

    # If the msg list is not 1
    else:

      # Gets the second item from the list
      second_word = msg_list[1]

      # Gets the number of results
      number_of_results = int(second_word) if second_word.isdigit() else 100

      # Calls the API to get the list of transactions
      transactions = etherscan_api.get_normal_transactions(msg_list[0], number_of_results)

    # Gets the timezone
    timezone = get_timezone_from_db(message.chat.id)
    
    # Gets the details of the transactions
    details = [transaction.read(timezone, False) for transaction in transactions]

    # Sends the message to the user and exits the function
    return split_message(message.chat.id, "\n\n".join(details))

  # Otherwise, sends a message to the user to input their transaction hash
  bot.send_message(message.chat.id, "Please enter your wallet address.")

  # Registers this function as the next step handler
  bot.register_next_step_handler(message, get_transactions_handler)


@bot.message_handler(commands=["getpasttxs", "getpasttx"])
def get_past_transactions_handler(message: Message) -> None:
  """Function to handle the /getpasttxs command"""

  # Gets the text from the message
  msg = message.text

  # Removes the command
  msg = re.sub("/getpasttxs|/getpasttx", "", msg).strip()

  # Gets the timezone
  timezone = get_timezone_from_db(message.chat.id)

  # Checks if the message is not empty
  if msg:

    # Gets the list of words in the message
    msg_list = msg.split()

    # Checks if the length of the list is 1
    if len(msg_list) == 1:

      # Gets the list of transactions
      transactions = data_analytics.get_transactions_by_past_months(msg, 6, timezone)

    # If the msg list is not 1
    else:

      # Gets the second item from the list
      second_word = msg_list[1]

      # Gets the number of months
      number_of_months = int(second_word) if second_word.isdigit() else 6

      # Calls the API to get the list of transactions
      transactions = data_analytics.get_transactions_by_past_months(msg_list[0], number_of_months, timezone)
    
    # Gets the details of the transactions
    details = [transaction.read(timezone, False) for transaction in transactions]

    # Sends the message to the user and exits the function
    return split_message(message.chat.id, "\n\n".join(details))

  # Otherwise, sends a message to the user to input their transaction hash
  bot.send_message(message.chat.id, "Please enter your wallet address.")

  # Registers this function as the next step handler
  bot.register_next_step_handler(message, get_transactions_handler)


@bot.message_handler(commands=["getanalytics", "getanalytic"])
def get_analytics_handler(message: Message) -> None:
  """Function to handle the /getanalytics function"""

  # Gets the text from the message
  msg = message.text

  # Removes the command from the message
  msg = re.sub("/getanalytics|/getanalytic", "", msg).strip()

  # Gets the timezone
  timezone = get_timezone_from_db(message.chat.id)

  # Checks if the message is not empty
  if msg:

    # Gets the list of words in the message
    msg_list = msg.split()

    # Checks if the length of the list is 1
    if len(msg_list) == 1:

      # Gets the graph
      graph = data_analytics.get_graph(msg, 6, timezone)

    # If the msg list is not 1
    else:

      # Gets the second item from the list
      second_word = msg_list[1]

      # Gets the number of months
      number_of_months = int(second_word) if second_word.isdigit() else 6

      # Makes the number of months 6 if it's more than 6
      number_of_months = 6 if number_of_months > 6 else number_of_months

      # Calls the API to get the graph
      graph = data_analytics.get_graph(msg_list[0], number_of_months, timezone)
    
    # Sends the graph to the user and exits the function
    return bot.send_message(message.chat.id, f"```{graph}```", parse_mode="Markdown")

  # Otherwise, sends a message to the user to input their transaction hash
  bot.send_message(message.chat.id, "Please enter your wallet address.")

  # Registers this function as the next step handler
  bot.register_next_step_handler(message, get_analytics_handler)


def split_message(chat_id: Union[str, int], bot_msg: str) -> None:
  """Function to split the message based on new lines"""

  # Gets the length of the bot message
  bot_msg_len = len(bot_msg)
  
  # Checks the length of the bot message
  if bot_msg_len < 4097:

    # Immediately sends the message to the user
    return bot.send_message(chat_id, bot_msg)

  # Otherwise, initialise the start and end index for the message
  start_index = 0
  end_index = 4097

  # The regular expression to find the last new line character
  new_line_regex = re.compile(r"\n(?=.*\Z)")

  # Iterates the message while the end index is less than the length of the message
  while end_index < bot_msg_len:

    # Gets the message slice
    msg_slice = bot_msg[start_index : end_index]

    # Finds the very last new line character
    last_new_line = new_line_regex.search(msg_slice)

    # Gets the index of the last new line and add 1 to get the character after it (adds the start index because the index is used in the full bot message)
    last_new_line_index = last_new_line.end() + 1 + start_index

    # Sends the message slice to the user
    bot.send_message(chat_id, bot_msg[start_index : last_new_line_index])

    # Change the start index to the index of the last new line
    start_index = last_new_line_index

    # Change the end index to 4097 characters above the start index
    end_index = start_index + 4097

  # Sends the final slice of the message if it's not empty
  if len(bot_msg[start_index:]) != 0:
    bot.send_message(chat_id, bot_msg[start_index:])
    


