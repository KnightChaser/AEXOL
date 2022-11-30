import os
import discord

#############################################################################

# Initialization.

bot = discord.Bot()

with open("./asset/token/token.txt") as token_file:
    TOKEN = token_file.read()

for _cogs_filename in os.listdir("./cogs"):
    cog_name = _cogs_filename.split(".")[0]
    bot.load_extension(f"cogs.{cog_name}")

@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online")

##############################################################################

# @bot.slash_command(name = "hello", description = "인사하기")
# async def hello(ctx):
#     await ctx.respond(f"{ctx.author.name} 님 반가워요! 저는 AEXOL|HYPER 입니다!")
    
bot.run(TOKEN)