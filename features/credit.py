import discord

async def display_owner_credit(ctx):
    embed = discord.Embed(title = f"📋 크레딧", color = 0xD5E6BB)
    embed.add_field(name = "제작자", value = "LUEXR", inline = False)
    embed.add_field(name = "Github 레포지토리", value = "[https://github.com/x3onkait/AEXOL](https://github.com/x3onkait/AEXOL)", inline = False)
    embed.add_field(name = "제작자 블로그", value = "[https://blog.naver.com/luexr](https://blog.naver.com/luexr)", inline = False)
    embed.add_field(name = "사용 언어", value = "Python **3**", inline = False)
    embed.set_footer(text = "SYFF{1_L0vE_D3ep_D@Rk_F4NTa$Y_n_FR!3NCh_Fr135}")
    await ctx.reply(embed = embed)