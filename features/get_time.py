import time
import discord

async def send_current_formatted_time(ctx):
    
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
    
    await ctx.reply(embed = embed)