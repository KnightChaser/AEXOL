

class VoiceChannel:

    def __init__(self, ctx):
        self.ctx = ctx

    async def join_voice_channel(ctx):
        if ctx.author.voice is None:
                await ctx.reply("먼저 음성 채널에 들어가서 다시 저를 호출해 주세요.")
        else:
            voice_channel = ctx.author.voice.channel
            if ctx.voice_client is None:
                await voice_channel.connect()
                voice_channel = ctx.author.voice.channel                        # refresh variable
                await ctx.reply(f"음성 채널(`{voice_channel}`)에 들어갔어요.")
            else:
                await ctx.voice_client.move_to(voice_channel)
                await ctx.reply(f"음성 채널(`{voice_channel}`)로 이동했어요.")

    async def leave_voice_channel(ctx):
        if ctx.voice_client:
            await ctx.guild.voice_client.disconnect()
            await ctx.reply(f"음성 채널에서 나왔어요.")
        else:
            await ctx.reply(f"저는 아직 음성채널에 있지 않아요.")