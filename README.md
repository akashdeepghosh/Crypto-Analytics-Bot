# NFT-Hackathon

![Crypto Analytics Bot](https://i.imgur.com/2CzbS2q.png)
**Vision:**

Crypto Analytics Bot enables anyone to easily access their wallet data and get details about their NFT. Our vision is to enable everyone to get access to free Crypto analytics right from Discord and Telegram.

**Description:**

- • What if you had the chance to buy/sell/send NFTs to anyone instantly by just mentioning them in Discord and Telegram?
- • What if you can get multiple roles just by verifying you are a holder?
- • What if you can get access to data analytics tools for your wallet right in Discord and Telegram?
- • What if you can check the prices of any token instantly?

We have a solution for you. We have made a Discord and a Telegram bot that is capable to fetch on-chain data and show it directly to users in Discord and Telegram. We have a good set of tools for Data Analytics right now and will continue to improve it as we move ahead. 
**- Then we are planning to integrate buy/sell NFTs directly from Discord and Telegram.**

Commands available right now:

**Discord:**

**/ethbalance**
-> Get ETH Balance for any wallet

**/convert**
-> Convert ETH to USD and USD to ETH (Other pairs are in the roadmap)

**/gettxdetails**
-> Get transaction details using a transaction hash

**/get_nft_owners**
-> Get NFT Owners for any NFT contract and Token ID

**/token_id_metadata**
-> Get NFT Metadata from the NFT contract and Token ID

**Telegram:**

**/changetimezone**
-> Changes your timezone

**/currenttimezone**-> Shows the current timezone the bot is set to

**/ethbalance \<address\>**
-> Gets the account balance of your ethereum wallet

**/ethprice**
-> Gets the current price of Ether in USD

**/convert**
-> Converts USD to Ether and vice versa

**/gettxdetails \<transaction hash\>**
-> Gets the details of the transaction

**/gettxs \<address\> \<number of transactions (n) (optional)\>**
-> Gets the past n transactions (defaults to the past 100 transactions)

**/getpasttxs \<address\> \<number of months (n) (optional)\>**
-> Gets the transactions for the past n months (defaults to 6 months)

**/getanalytics \<address\> \<number of months (n) (optional, maximum of 6 months)\>**
-> Gets the analytics graph for given number of months (defaults to the maximum of 6 months)


**APIs Used:**

- Etherscan API
- Moralis API

**Platform Used:**
- Replit (for both Discord and Telegram bot hosting)

**Future Roadmap:**
- 1 - Full multiple wallet integration and verification with Discord Roles - MetaMask, WalletConnect etc.
- 2 - Give users the feasibility to buy and sell NFT right from discord and telegram after verification. We will set up some security verification for it so that if the discord/telegram account gets compromised, the hackers can’t buy or sell the NFTs. - OpenSea SDK
- 3 - Add many more wallet analysis features.
- 4 - Real-time prices of multiple crypto tokens. - CoinGecko API
- 5 - Wallet Whitelist for NFTs. Right now, the users use Discord and Telegram for most NFT projects to interact with the developers of the project and other users. The whitelisting process is not so streamlined and there is no solution available for it right now. We will solve the entire process with our bot.
- 6 - OpenSea sales tracking. We will integrate Opensea sales in our bot so that whenever a new event occurs (buy/sell) it will announce on a Discord channel and Telegram channel. - OpenSea API
- 7 - Integrate other blockchain platforms like Solana and Polygon.
