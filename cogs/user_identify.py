import discord
from discord.ext import commands

class UserIdentify(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    user = discord.SlashCommandGroup(name = "user", description = "유저 정보에 대한 명령을 실행합니다")

    @user.command(description = "인사하기")
    async def hello(self, ctx):
        await ctx.respond(f"**{ctx.author}**님 안녕하세요! 저는 **AEXOL** 입니다!")


def setup(bot):
    bot.add_cog(UserIdentify(bot))