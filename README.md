# AEXOL 


![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Ubuntu](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)
![Windows](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)
![Discord](https://img.shields.io/badge/Discord-%235865F2.svg?style=for-the-badge&logo=discord&logoColor=white)
 
A light **Discord bot with simple useful features** that is intended to run in 24/7-operating Linux or Windows server environment **for Korean(🇰🇷) Discord users**, written in Python, objected to impose object-oriented programming if able. I made it for a personal hobby 

This is the 3rd official challenge to make sustainable and scalable Discord chatbot with Python.


### 📋 Projects

 - [ ] (★)Turn from prefix command system to slash(`/`) command system with user-guiding (Discord.py 2)
 - [ ] (★)Employ buttons, selection bars or input forms **entirely** to make the bot easier (Discord.py 2)
 - [x] Basic features
     - [x] Alive check (hello)
     - [x] Exception check
     - [x] Bot status change
     - [x] Automatic user authorization and access control for special commands
     - [x] Help feature
         - [x] detailed help messages for specified commands
         - [x] dictionary-based help message data structure
         - [x] easily-scalable and editable help messages
     - [x] Get current time
         - [ ] With optional variable for different time zones
     - [x] Ping to specified target (**prevent possible command injection vulnerability**)
 - [x] Voice channel
     - [x] Join / leave / move channel **per server**
     - [x] Streaming music without saving as `youtube-dl` **per server**
     - [x] Affordable streaming quality (honestly depended on the server performance) **per server**
     - [x] Add, show, delete, edit, clear music elements to the queue **per server**
     - [x] Voice channel related exception catch
     - [ ] Show current playing music
     - [ ] Add music playing buttons
 - [x] Real-time cryptocurrencies information (with Upbit public API)
     - [x] Check market code availability
     - [x] Get basic ticker information
     - [x] Get basic candle chart
     - [x] Pretty Embed
     - [x] Customize candle chart like font
     - [x] Support KRW, BTC, USDT(Tether) market
     - [ ] ~~User-input-driven candle chart customization (Candle qty, Period per candle)~~
     - [x] Sort cryptocurrencies list (trade price, trade volume, change rate, etc...)
 - [ ] Naver finance (Unofficial way)
     - [x] Avoid excessive requests to gather informations
     - [x] Major domestic(Korean) indexes (KOSPI, KOSDAQ, KPI200)
     - [ ] Stock search feature
     - [ ] (Listed) Company information search feature (with KRX dataset if it's technically possible)
 - [ ] Google finance (stocks, indexes, news...)
     - [ ] Major stocks
     - [ ] Major indexes
     - [ ] Major news
 - [ ] Enhance the automatic execution shell script (`run.sh`) to find lacked package dependencies
 - [ ] Live weather and forecasts
 - [ ] Customizing prefix (default : `axl! _commands_ *args`)
     - [ ] Save as a database, with MySQL or SQLite
 - [x] Provides detailed guides (`axl! help [args]`)
