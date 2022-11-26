import discord
from discord.ext import commands
from features import _available
from features.cryptocurrencies.get_crypto_market import *
from features.credit import *
from features.get_time import *
from features.google_index_search import *
from features.help import *
from features.send_ping import *
from features.finance.indexes import *
from features.voice_channel import *
import validators

import sys
sys.path.append("./features/voice")

##########################################################

TOKEN_FILE = open("./asset/token/token.txt", 'r')
TOKEN      = TOKEN_FILE.readline()
TOKEN_FILE.close()

bot = commands.Bot(command_prefix = 'axl! ', help_command=None, intents=discord.Intents.all())

##########################################################

@bot.event
async def on_ready():
    print(f'logged in as {bot.user}')

##########################################################

@bot.command(name = "change_status")
@commands.is_owner()
async def change_status(ctx, *args):
    available_status = {"online" : "온라인",
                        "offline" : "오프라인", 
                        "idle" : "대기", 
                        "do_not_disturb" : "방해금지",
                        "invisible" : "숨김"}
    request = args[0]
    await bot.change_presence(status = getattr(discord.Status, request))
    embed = discord.Embed(title = "상태 전환 성공", 
                        description = f"봇({bot.user})를 성공적으로 **{available_status[request]}({request})** 상태로 전환했습니다.", 
                        color = 0x00FFDB)
    await ctx.reply(embed = embed)

@bot.command(name = "credit")
async def show_credit(ctx):
    await display_owner_credit(ctx)

@bot.command(name = "crypto")
async def get_cryptocurrency_market_info(ctx, *args):

    # if len(args) != 1 or args == "":
    #     await ctx.reply("마켓 코드를 정확하게 입력해 주세요. `[통화]-[암호화폐]` 형태로 입력해주시면 됩니다. (ex. `KRW-BTC`, `BTC-ETH`)")
    #     return

    # await get_crypto_info(ctx, *args)

    if len(args) == 2 and args[0] == "market":
        try:
            crypto_market_code = args[1]
            await get_crypto_info(ctx, crypto_market_code)
        except:
            await ctx.reply("마켓 코드를 정확하게 입력해 주세요. 자세한 내용은 도움말을 참조하세요. (`axl! help crypto`)")
    elif len(args) == 4 and args[0] == "rank":
        try:
            crypto_market_fiat      = args[1]
            sort_criteria           = args[2]
            sort_order_direction    = args[3]
            await get_crypto_ranking_by(ctx, crypto_market_fiat, sort_criteria, sort_order_direction)
        except:
            await ctx.reply("정보를 처리하는데 실패했습니다. 매개변수가 잘못된 것 같습니다. 자세한 내용은 도움말을 참조하세요. (`axl! help crypto`)")
    else:
        await ctx.reply("올바른 인자가 아닙니다. 자세한 내용은 도움말을 참조하세요. (`axl! help crypto`)")


@bot.command(name = "hello")
async def hello(ctx):
    await ctx.reply(f"반가워요! **{ctx.author.name}**님! 저는 **{bot.user}** 입니다!")


@bot.command(name = "google")
async def hello(ctx, *args):

    if len(args) != 1 or args == "":
        await ctx.reply("검색 키워드를 한 단어로 입력해주시고, 검색어에 공백이 있다면 `\"...\"` 형태로 검색어 양 끝에 따옴표를 넣어주세요. (ex. `\"Python 3\"`)")
        return

    await get_google_search_index(ctx, *args)


@bot.command(name = "help")
async def help(ctx, *args):
    await get_help(ctx, *args)


@bot.command(name = "ping")
async def ping(ctx, *args):
    if not args or len(args) != 1:
        # no input
        await ctx.reply(f"`ping` 명령어를 위한 제대로 된 인수가 주어지지 않은 것 같아요. (도움말 참조)")
    else:
        await send_ping(ctx, args[0])
        

@bot.command(name = "finance")
async def finance(ctx, *args):
    if len(args) == 1 and args[0] == "index":
        view = IndexInfoMenu(ctx = ctx)
        await ctx.reply(view = view)


@bot.command(name = "time")
async def get_time(ctx):
    await send_current_formatted_time(ctx)


@bot.command(name = "voice_channel")
async def voice_channel(ctx, *args):
    server_id      = ctx.guild.id
    # voice_channel [args...]
    if not args:
        #no input
        await ctx.reply(f"`voice_channel` 명령어를 위한 제대로 된 인수가 주어지지 않은 것 같아요. (도움말 참조)")
    else:
        # voice_channel join
        if args[0] == "join" and len(args) == 1:
            # await voice.join_voice_channel(ctx)
            await VoiceChannel.join_voice_channel(ctx)
        # voice_channel leave
        elif args[0] == "leave" and len(args) == 1:
            await VoiceChannel.leave_voice_channel(ctx)
        # voice_channel playlist add [youtube_url]
        elif args[0] == "playlist" and args[1] == "add" and validators.url(args[2]) and len(args) == 3:
            try:
                requested_url = args[2]
                await voice_channel_playlist(ctx, server_id, "add_queue", requested_url)
            except:
                await ctx.reply("올바른 요청 형식이 아니어서 오류가 발생한 것 같아요. (중복 재생 시도, 처리 오류, 인터넷 연결 불안정 / 도움말 참조)")
        # voice_channel playlist show
        elif args[0] == "playlist" and args[1] == "show" and len(args) == 2:
            await voice_channel_playlist(ctx, server_id, "show_queue")
        # voice_channel playlist delete [index]
        elif args[0] == "playlist" and args[1] == "delete" and len(args) == 3:
            index = args[2]
            if index == "*":                    # delete everything
                pass
            else:
                try:
                    index = int(args[2])        # delete something (designate by index number of the list)
                except ValueError:
                    return
            # await delete_element_in_queue(ctx, server_id, index, True)
            await voice_channel_playlist(ctx, server_id, "delete_queue", index)
        # voice_channel playlist play
        elif args[0] == "playlist" and args[1] == "play" and len(args) == 2:
            await voice_channel_playlist(ctx, server_id, "play_queue")
        # voice_channel playlist pause
        elif args[0] == "playlist" and args[1] == "pause" and len(args) == 2:
            await voice_channel_playlist(ctx, server_id, "pause_media")
        # voice_channel playlist resume
        elif args[0] == "playlist" and args[1] == "resume" and len(args) == 2:
            await voice_channel_playlist(ctx, server_id, "resume_media")
        # voice_channel playlist stop
        elif args[0] == "playlist" and args[1] == "skip" and len(args) == 2:
            await voice_channel_playlist(ctx, server_id, "skip_media")
        elif args[0] == "playlist" and args[1] == "stop" and len(args) == 2:
            await voice_channel_playlist(ctx, server_id, "stop_media")
        else:
            await ctx.reply(f"`voice_channel` 명령어를 위한 제대로 된 인수가 주어지지 않은 것 같아요. (도움말 참조)")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.NotOwner):
        embed = discord.Embed(title = "권한 부족", 
                            description = f"제시하신 명령어 `{ctx.message.content}`는 관리자만 실행할 수 있습니다.", 
                            color = 0xFF0000)
        await ctx.reply(embed = embed)
    else:
        embed = discord.Embed(title = "예외 발생", 
                            description = "명령어가 올바르지 않거나 실행 과정에서 오류가 발생했습니다.", 
                            color = 0xFF0000)
        embed.add_field(name = "에러 로그", value = f"`{error}`", inline = True)
        embed.set_footer(text = "제대로 된 실행에도 오류가 계속되면 관리자에게 연락하세요.")
        await ctx.reply(embed = embed)
    pass

bot.run(TOKEN)