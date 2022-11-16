from pythonping import ping
import discord

async def send_ping(ctx, target):
    request_qty = 5
    try:

        response_list = ping(target, count = request_qty)
        
        # 메시지
        if response_list.stats_success_ratio == 1:
            message = "성공(Success)"
        elif 0 < response_list.stats_success_ratio < 1:
            message = "부분 성공(Partial)"
        else:
            message = "실패(Failed)"

        result = {
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
        # illegal input detected
        result = "illegal input for ping"
    finally:
        # just relay the value ctx to execute next function send_ping_result that uses Discord.py functions
        await send_ping_result(ctx, result)

async def send_ping_result(ctx, result):

    ping_result = result
    
    if ping_result == "illegal input for ping":
        # illegal input
        await ctx.reply(f"`ping` 명령어를 위한 인수가 적절하지 않은 것 같아요. (도움말 참조)")
    else:
        embed = discord.Embed(title = f"`ping` 보내기", color = 0x00FFDB)
        embed.add_field(name = "목적지", value = f"`{result['target']}`", inline = False)
        embed.add_field(name = "결과", value = f"**{ping_result['message']}** ({ping_result['success_ratio_percentage']}%)", inline = False)
        embed.add_field(name = "RTT", value = f"**평균** : {ping_result['rtt_avg_ms']}ms, **최대** : {ping_result['rtt_max_ms']}ms, **최소** : {ping_result['rtt_min_ms']}ms")
        embed.set_footer(text = "IP주소나 URL로 ping을 시도할 수 있어요.")
        await ctx.reply(embed = embed)