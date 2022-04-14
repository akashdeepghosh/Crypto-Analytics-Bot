# Main module to run everything

import logging, threading
import telegram_bot, discord_bot
# import keep_alive


# Set up logging
logging.basicConfig(
  level = logging.DEBUG,
  format = "%(levelname)s - %(asctime)s: %(message)s"
)

# Calls the keep_alive function to keep the bots alive
# keep_alive.keep_alive()

# Function to run the bots
def run_bots() -> None:

  # Starts the telegram bot in a thread
  threading.Thread(target=telegram_bot.bot.infinity_polling).start()
  
  # Starts the discord bot
  discord_bot.bot.run(discord_bot.discord_token)
      
  
# Name safeguard
if __name__ == "__main__":

  # Run the bots
  run_bots()