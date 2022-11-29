import discord
from discord.ext import commands
from discord.commands import Option
import time

class Time(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        
    time = discord.SlashCommandGroup(name = "time", description = "시간을 알아봅니다")

    @time.command(description = "서버 시간 확인하기")
    async def server(self, ctx):
    
        tm = time.localtime(time.time())

        year    = tm.tm_year
        month   = tm.tm_mon
        day     = tm.tm_mday
        hour    = tm.tm_hour
        minute  = tm.tm_min
        second  = tm.tm_sec

        formatted_time_string = f"{year}년 {month}월 {day}일 {hour}시 {minute}분 {second}초"

        embed = discord.Embed(title = "현재 시간", 
                            description = f"{formatted_time_string}", 
                            color = 0x00FFDB)
        embed.set_footer(text = "한국표준시(KST) 기준")
        
        await ctx.respond(embed = embed)

def setup(bot):
    bot.add_cog(Time(bot))