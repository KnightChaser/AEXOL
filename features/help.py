import discord
from . import _available

async def get_help(ctx, *args):
    
    if not args:
        available_commands_list = ""
        for _dataline in _available.supported_commands:
            available_commands_list += f"`{_dataline}` "
        embed = discord.Embed(title = "명령어 도움말", color = 0xE4F9F5)
        embed.add_field(name = "사용 가능한 명령어", value = f"{available_commands_list}", inline = False)
        embed.add_field(name = "공통 명령어 형식(prefix)", value = f"`axl! [command] [args...]`", inline = False)
        embed.add_field(name = "특정 명령어 자세하게 알아보기", value = f"`!help [command]`\n(`[command]`에서 명령어 앞의 axl!는 붙이지 마세요.)", inline = False)
        await ctx.reply(embed = embed)

    elif len(args) == 1:
        request = args[0]
        if request in _available.supported_commands:
            detailed_guide              = _available.supported_commands[request]
            detailed_guide_description  = detailed_guide["description"]
            detailed_guide_usage        = detailed_guide["usage"]
            detailed_guide_privilege    = detailed_guide["privilege"]
            embed = discord.Embed(title = f"자세한 명령어 도움말 `({request})`", color = 0xE4F9F5)
            embed.add_field(name = "명령어 설명", value = f"{detailed_guide_description}", inline = False)
            embed.add_field(name = "명령어 형식", value = f"`{detailed_guide_usage}`", inline = False)
            embed.add_field(name = "명령어 권한", value = f"`{detailed_guide_privilege}`", inline = False)
            
            if "detailed_descriptions" in detailed_guide:
                for _seq in range(len(detailed_guide["detailed_descriptions"])):
                    detailed_descriptions_title     = detailed_guide["detailed_descriptions"][_seq]["title"]
                    detailed_descriptions_content   = detailed_guide["detailed_descriptions"][_seq]["content"]
                    embed.add_field(name = f"{detailed_descriptions_title}", value = f"{detailed_descriptions_content}", inline = False)

            embed.set_footer(text = "명령어 권한이 administrator인 경우 권한이 있는 관리자만 실행할 수 있어요.")
            await ctx.reply(embed = embed)
    else:
        await ctx.reply(f"명령어 형식이 올바르지 않은 것 같아요. (`axl! help [command]`)")