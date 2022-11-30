import discord
from discord.ext import commands
from discord.commands import Option
from pythonping import ping

class Ping(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        
    ping = discord.SlashCommandGroup(name = "ping", description = "통신 지연 시간 측정")

    @ping.command(description = "이 봇과 통신 지연 시간 측정")
    async def bot(self, ctx):
        embed = discord.Embed(title = f"지연 체크", color = 0x00FFDB)
        embed.add_field(name = "\u200b", value = f"**🏓 Pong!** ...  {ctx.author.name}님과 저와는 **{round(self.bot.latency * 1000)}ms** 만큼 통신 지연이 있어요.", inline = False)
        await ctx.respond(embed = embed)

    @ping.command(description = "타겟과 통신 지연 시간 측정")
    async def target(self, 
                        ctx,
                        target: Option(str, "IP주소나 도메인 주소"),
                    ):
        request_qty = 5

        try:
            response_list = ping(target, count = request_qty)

            if response_list.stats_success_ratio == 1:
                message = "성공(Success)"
            elif 0 < response_list.stats_success_ratio < 1:
                message = "부분 성공(Partial)"
            else:
                message = "실패(Failed)"

            ping_result = {
                "target"                    : target,
                "rtt_avg_ms"                : response_list.rtt_avg_ms,
                "rtt_max_ms"                : response_list.rtt_max_ms,
                "rtt_min_ms"                : response_list.rtt_min_ms,
                "packets_sent"              : response_list.stats_packets_sent,
                "packets_returned"          : response_list.stats_packets_returned,
                "success_ratio_percentage"  : response_list.stats_success_ratio * 100,
                "message"                   : message
            }
        except:
            ping_result = "illegal input for ping"
        finally:
            # just relay the value and let the user know
            if ping_result == "illegal input for ping":
                # illegal input
                await ctx.respond(f"`ping` 명령어를 위한 인수가 적절하지 않은 것 같아요. (도움말 참조)")
            else:
                embed = discord.Embed(title = f"`ping` 보내기", color = 0x00FFDB)
                embed.add_field(name = "목적지", value = f"`{ping_result['target']}`", inline = False)
                embed.add_field(name = "결과", value = f"**{ping_result['message']}** ({ping_result['success_ratio_percentage']}%)", inline = False)
                embed.add_field(name = "RTT", value = f"**평균** : `{ping_result['rtt_avg_ms']}ms`, **최대** : `{ping_result['rtt_max_ms']}ms`, **최소** : `{ping_result['rtt_min_ms']}ms`")
                embed.set_footer(text = "IP주소나 URL로 ping을 시도할 수 있어요.")
                await ctx.respond(embed = embed)
            

def setup(bot):
    bot.add_cog(Ping(bot))