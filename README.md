# AEXOL 


![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Ubuntu](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)
![Windows](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)
![Discord](https://img.shields.io/badge/Discord-%235865F2.svg?style=for-the-badge&logo=discord&logoColor=white)
 
A light **Discord bot with simple useful features** that is intended to run in 24/7-operating Linux or Windows server environment **for Korean(🇰🇷) Discord users**, written in Python, objected to impose object-oriented programming if able. I made it for a personal hobby.

This is the 3rd official challenge to make sustainable and scalable Discord chatbot with Python.

This bot supports features below currently
 - Alive check
 - Easily scalable `help` command feature
 - Get current time
 - ping to the specified target
 - Voice channel and live music playing with queue
 - Google index searching, sorting top results and related simple statistics
 - Authorization for specific commands
 - Exception catch


Improvement projects
 - [ ] Get current time with optional variable for different time zones
 - [x] Real-time cryptocurrencies information (with Upbit public API)
     - [ ] Check market code availability
     - [x] Get basic ticker information
     - [x] Get basic candle chart
     - [x] Pretty Embed
     - [x] Customize candle chart like font
     - [x] Support KRW, BTC, USDT(Tether) market
     - [ ] User-input-driven candle chart customization (Candle qty, Period per candle)
     - [ ] Sort cryptocurrencies list (trade price, trade volume, change rate, etc...)
 - [ ] Google finance (stocks, indexes, news...)
     - [ ] Major stocks
     - [ ] Major indexes
     - [ ] Major news
 - [ ] Enhance the automatic execution shell script (`run.sh`) to find lacked package dependencies
 - [ ] Live weather and forecasts
 - [ ] Customizing prefix (default : `axl! _commands_ *args`)
     - [ ] Save as a database, with MySQL or SQLite
