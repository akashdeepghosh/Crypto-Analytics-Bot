import os
import discord
from discord.ext import commands
from discord.commands import Option, OptionChoice
import etherscan_api
import data_analytics

# DISCORD TOKEN
discord_token = os.environ['DISCORD_TOKEN']

# Bot prefix
bot = commands.Bot(command_prefix='>')

# Create a test server for faster slash command implementation
test_guild_id = [962620301055778866]

# convert hexadecimal to decimal
def hex_to_dec(hex_string):
  return int(hex_string, 16)

# Slash command for ETH Balance
@bot.slash_command(name="ethbalance", guild_ids=test_guild_id)
async def ethbalance(ctx, address: Option(str, 'Enter your ETH address', required = True)):
  """GET ETH BALANCE"""

  data = etherscan_api.get_ether_balance(address)
  converted_data = etherscan_api.convert_eth_to_usd(data)
  embed = discord.Embed(title="Crypto Analytics bot", color=discord.Color.dark_red())
  embed.add_field(name="ETH Balance", value=f"ETH balance of {address} is **{data} ETH** (**{converted_data} USD**)")
  embed.set_footer(text="Data fetched from Etherscan.io and Coingecko.com")
  await ctx.respond(embed=embed)

# Slash command for ETH to USD and USD to ETH with OptionChoice
@bot.slash_command(name="convert", guild_ids=test_guild_id)
async def convert(ctx, amount: Option(str, 'Enter the amount to convert', required = True), choice: Option(str, 'Enter the conversion type', required = True, choices = [OptionChoice(name="ETH to USD", value="eth_to_usd"), OptionChoice(name="USD to ETH", value="usd_to_eth")])):
  
  """CONVERT ETH TO USD OR USD TO ETH"""

  if choice == "eth_to_usd":
    data = etherscan_api.convert_eth_to_usd(amount)
    embed = discord.Embed(title="Crypto Analytics bot", color=discord.Color.dark_red())
    embed.add_field(name="ETH to USD", value=f"{amount} ETH is **{data} USD**")
    embed.set_footer(text="Data fetched from Coingecko.com")
    await ctx.respond(embed=embed)
  elif choice == "usd_to_eth":
    data = etherscan_api.convert_usd_to_eth(amount)
    embed = discord.Embed(title="Crypto Analytics bot", color=discord.Color.dark_red())
    embed.add_field(name="USD to ETH", value=f"{amount} USD is **{data} ETH**")
    embed.set_footer(text="Data fetched from Coingecko.com")
    await ctx.respond(embed=embed)
  else:
    await ctx.respond("Please enter a valid choice")

# Slash command for get transaction details
@bot.slash_command(name="gettxdetails", guild_ids=test_guild_id)
async def gettxdetails(ctx, txhash: Option(str, 'Enter your transaction hash', required = True)):
  """GET TRANSACTION DETAILS"""
  data = etherscan_api.get_transaction_receipt(txhash)

  embed = discord.Embed(title="Crypto Analytics Bot", color=discord.Color.dark_red())
  embed.add_field(name="From", value=f"{data['from']}", inline = False)
  embed.add_field(name="To", value=f"{data['to']}", inline = False)
  embed.add_field(name="Gas Used", value=f"{hex_to_dec(data['gasUsed'])}", inline = False)
  embed.add_field(name="Status", value="Success" if hex_to_dec(data['status']) == 1 else "Failed", inline = False)
  embed.add_field(name="Etherscan Link", value=f"https://etherscan.io/tx/{txhash}", inline = False)
  embed.set_footer(text="Data fetched from Etherscan.io")
  await ctx.respond(embed=embed)

# Implement moralis_api
@bot.slash_command(name="get_nft_owners", guild_ids=test_guild_id)
async def get_nft_owners(ctx, address: Option(str, 'Enter the NFT contract address', required = True), token_id: Option(str, 'Enter NFT token id', required = True)):
  """GET NFT OWNERS"""
  data = etherscan_api.get_nft_owners(address, token_id)
  embed = discord.Embed(title="Crypto Analytics Bot", color=discord.Color.dark_red())
  embed.add_field(name="Name", value=f"{data['name']}", inline = False)
  embed.add_field(name="Symbol", value=f"{data['symbol']}", inline = False)
  embed.add_field(name="Token Address", value=f"{data['token_address']}", inline = False)
  embed.add_field(name="Amount", value=f"{data['amount']}", inline = False)
  embed.set_footer(text="Data fetched from Moralis.io")
  await ctx.respond(embed=embed)

@bot.slash_command(name="token_id_metadata", guild_ids=test_guild_id)
async def token_id_metadata(ctx, address: Option(str, 'Enter the NFT contract address', required = True), token_id: Option(str, 'Enter NFT token id', required = True)):
  """GET NFT METADATA"""
  data = etherscan_api.get_nft_metadata(address, token_id)
  embed = discord.Embed(title="Crypto Analytics Bot", color=discord.Color.dark_red())
  embed.add_field(name="Name", value=f"{data['name']}", inline = False)
  embed.add_field(name="Symbol", value=f"{data['symbol']}", inline = False)
  embed.add_field(name="Token Address", value=f"{data['token_address']}", inline = False)
  for i in data['metadata']:
    embed.add_field(name=i['key'], value=f"{i['value']}", inline = False)
  embed.set_footer(text="Data fetched from Moralis.io")
  await ctx.respond(embed=embed)


bot.run(discord_token)
