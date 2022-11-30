import discord
from discord import Option
from discord.ext import commands
import time
import calendar

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

    @time.command(description = "한 달 달력 보기")
    async def calender_month(self,
                             ctx,
                             year: Option(int, "년도"),
                             month: Option(int, "달")):
        if 0 <= year <= 1000000000000 and 1 <= month <= 12:
            embed = discord.Embed(title = "📅 달력", color = 0x00FFDB)
            embed.add_field(name = f"{year}**년** {month}**월**", value = f"```\n{calendar.month(year, month)}\n```")
            await ctx.respond(embed = embed)
        else:
            # wrong year/month input
            await ctx.respond(f"유효한 시간(년/월)을 입력해주세요. 년도는 `0` ~ `1000000000000`, 월은 `0` ~ `12` 범위의 정수만 지원합니다.")

def setup(bot):
    bot.add_cog(Time(bot))