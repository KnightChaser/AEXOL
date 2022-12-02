import discord
from discord import Option
from discord.ext import commands
from components.finance.get_crypto_info import get_crypto_info, get_crypto_ranking_by

class finance(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    finance = discord.SlashCommandGroup(name = "finance", description = "금융 정보 조회")


    @finance.command(description = "암호화폐 시세 조회")
    async def crypto_market(self,
                            ctx,
                            fiat_currency: Option(str, "거래통화(마켓)", choices = ["KRW", "BTC", "USDT"]),
                            crypto_symbol: Option(str, "조회할 암호화폐 종목(ex. BTC)")):

        market_code = f"{fiat_currency}-{crypto_symbol}"
        result_as_embed = await get_crypto_info(ctx, market_code)
        await ctx.respond(embed = result_as_embed)

    @finance.command(description = "암호화폐 통계 조회")
    async def crypto_rank(self,
                          ctx,
                          fiat_currency: Option(str, "거래통화(마켓)", choices = ["KRW", "BTC", "USDT"]),
                          sort_criteria: Option(str, "조회 기준", choices = ["시가(Opening Price)", "고가(High Price)", "저가(Low Price)", "현재가(Trade Price)",
                                                                            "전일 종가(UTC 0시 기준)", "시세 변화액(24시간)", "시세 변화율(24시간)",
                                                                            "누적 거래대금(UTC 0시 기준)", "누적 거래대금(24시간)"]),
                          sort_direction: Option(str, "방향", choices = ["오름차순(ascending)", "내림차순(descending)"])):

        sort_criteria_conversion = {
            "시가(Opening Price)"           : "opening_price",
            "고가(High Price)"              : "high_price",
            "저가(Low Price)"               : "low_price",
            "현재가(Trade Price)"           : "trade_price",
            "전일 종가(UTC 0시 기준)"       : "prev_closing_price",
            "시세 변화액(24시간)"           : "signed_change_price",
            "시세 변화율(24시간)"           : "signed_change_rate",
            "누적 거래대금(UTC 0시 기준)"   : "acc_trade_price",
            "누적 거래대금(24시간)"         : "acc_trade_price_24h"
        }

        sort_direction_conversion = {
            "오름차순(ascending)"           : "ascending",
            "내림차순(descending)"          : "descending"  
        }

        result = await get_crypto_ranking_by(ctx, market = fiat_currency,
                                                  criteria = sort_criteria_conversion[sort_criteria],
                                                  order = sort_direction_conversion[sort_direction])
        await ctx.respond(result)


    
def setup(bot):
    bot.add_cog(finance(bot))