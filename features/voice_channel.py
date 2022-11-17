import discord
import youtube_dl
import datetime
import asyncio

active_voice_channal_class_dict = {}

class VoiceChannel:

    def __init__(self, ctx):
        self.ctx = ctx

    # Let the bot join the voice channel that author already joined
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

    # Let the bot leave the voice channel that author is joined
    async def leave_voice_channel(ctx):
        if ctx.voice_client:

            global active_voice_channal_class_dict

            if ctx.voice_client.is_playing():
                await ctx.reply(f"미디어 재생중이므로 재생목록의 내용을 모두 스킵하시거나 아니면 직접 연결을 끊어주세요.")
                return

            voice_client_music_instance_name = f"VoiceChannelMusic_{ctx.guild.id}"
            if voice_client_music_instance_name in active_voice_channal_class_dict.keys():
                voice_client_music_instance = active_voice_channal_class_dict[voice_client_music_instance_name]
                del voice_client_music_instance

            await ctx.guild.voice_client.disconnect()
            await ctx.reply(f"음성 채널에서 나왔어요.")
        else:
            await ctx.reply(f"저는 아직 음성채널에 있지 않아요.")

class VoiceChannelMusicPerServer():

    def __init__(self, ctx, server_id):
        self.ctx = ctx
        self.server_id = server_id
        self.music_queues = []

    async def add_queue(self, requested_url):

        if self.ctx.author.voice is None or self.ctx.voice_client is None:
            await self.ctx.reply("음성채널에 봇과 함께 같이 있는지 확인해주세요!")
            return

        allowable_youtube_link_detector = ['https://www.youtube.com/watch?v=', 'https://youtu.be/']
        if not requested_url.startswith(tuple(allowable_youtube_link_detector)) or "&start_radio" in requested_url or "&list" in requested_url or "&index" in requested_url:
        # when user gives playlist or station link of Youtube to play via this bot,
        # ffmpeg that is belonged to this tries to download everything in ths playlist so the task consumes so much time
        # and that's unexpected. so URL for playlist and station is blocked by these techincal issues.
            await self.ctx.reply(f"죄송해요! YouTube 영상 링크는 반드시 `https://www.youtube.com/watch?v=` 또는 `https://youtu.be/`로 시작해야 하며 YouTube Station 또는 플레이리스트 링크는 기술상 제약으로 인해 허용되지 않습니다.")
            return

        # check whether requested url is for available Youtube Video
        try:
            with youtube_dl.YoutubeDL() as ydl:
                ydl_extracted         = ydl.extract_info(requested_url, download = False)
                # video_thumbnail_chunk = ydl_extracted.get("thumbnails", None)
                # video_thumbnail       = video_thumbnail_chunk[len(video_thumbnail_chunk)]["url"]      # highest-resolution thumbnail
                video_information     = {
                    "video_url"         : ydl_extracted.get("webpage_url", None),
                    "video_title"       : ydl_extracted.get("title", None),
                    "video_uploader"    : ydl_extracted.get("uploader", None),
                    "video_duration"    : ydl_extracted.get("duration", None),
                    "video_thumbnail"   : ydl_extracted.get("thumbnail", None),
                    "video_view_count"  : ydl_extracted.get("view_count", None)
                }
        except:
            await self.ctx.reply(f"유효하지 않은 Youtube 동영상 링크인 것 같아요.")
            return

        # if self.music_queues == []:
        #     await self.ctx.send("현재 플레이리스트가 비어 있습니다.")

        self.music_queues.append(video_information)

        video_length_hhmmss    = str(datetime.timedelta(seconds = video_information['video_duration']))
        await self.ctx.send(f"💽 [**{video_information['video_title']}**]를 플레이리스트에 추가했어요. (재생 시간 : {video_length_hhmmss})")

    async def show_queue(self):

        if self.ctx.author.voice is None or self.ctx.voice_client is None:
            await self.ctx.reply("음성채널에 봇과 함께 같이 있는지 확인해주세요!")
            return
        
        server_name = self.ctx.guild.name

        local_playlist_string = "아직 아무것도 없어요..."           # <--- default message (when nothing inside the playlist)

        try:
            local_playlist = self.music_queues

            if local_playlist == None:
                pass
                # local_playlist_string = "아직 아무것도 없어요..."
            else:
                local_playlist_string = ""
                for index, music_info in enumerate(local_playlist):
                    index_number           = '{0: >4}'.format(index)
                    video_length_hhmmss    = str(datetime.timedelta(seconds = music_info['video_duration']))
                    local_playlist_string += f"#{index_number} : {music_info['video_title']} ({video_length_hhmmss})\n"

            if local_playlist_string == "":
                local_playlist_string = "아직 아무것도 없어요..."           # <--- playlist exists but nothing inside

        except KeyError:
            # if there is nothing on music_queues(0 items) and someone tries to show the playlist at that moment,
            # the keyerror will be occured because the key is NOT vaild for the playlist WITH NOTHING.
            pass
            # local_playlist_string = "아직 아무것도 없어요..."

        embed = discord.Embed(title = f"💽 재생목록", color = 0x00FFDB)
        embed.add_field(name = f"현재 서버 : {server_name}", value = f"```{local_playlist_string}```", inline = False)
        embed.set_footer(text = "등록된 순서에 따라, #0 부터 노래가 순서대로 재생됩니다.")

        await self.ctx.reply(embed = embed)

    async def delete_queue(self, index, notify):

        if self.ctx.author.voice is None or self.ctx.voice_client is None:
            await self.ctx.reply("음성채널에 봇과 함께 같이 있는지 확인해주세요!")
            return

        if index == "*":
            self.music_queues = []
            await self.ctx.reply("재생목록에 있는 내용을 모두 지웠어요.")
        else:
            try:
                target_title = self.music_queues[index]['video_title']
                self.music_queues.pop(index)
                if notify == True:
                    # if user deleted the element manually, we let the user know
                    await self.ctx.reply(f"[#{index}] **\"{target_title}\"**을 재생목록에서 삭제했어요.")
                else:
                    # if program deleted the element automatically, we don't need to let the user know
                    pass
            except IndexError:
                await self.ctx.reply("요청하신 번호에 해당하는 내용이 재생목록에 없어요. 한번 다시 확인해주세요!")

    async def play_queue(self):

        if self.ctx.author.voice is None or self.ctx.voice_client is None:
            await self.ctx.reply("음성채널에 봇과 함께 같이 있는지 확인해주세요!")
            return

        ffmpeg_options = {
            'options': '-vn -preset veryfast', 
            "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
        }

        while True:

            if self.music_queues != []:

                # Play until the playlist has nothing
                _song_data = self.music_queues[0]
                
                requested_url = _song_data['video_url']

                with youtube_dl.YoutubeDL() as ydl:
                    info = ydl.extract_info(requested_url, download = False)
                    URL = info['formats'][0]['url']

                # notify when music starts
                video_length_hhmmss  = str(datetime.timedelta(seconds = _song_data['video_duration']))
                embed = discord.Embed(title = f"▶ Now Playing", color = 0x00FFDB)
                embed.add_field(name = f"{_song_data['video_title']}", value = f"재생 시간 : `{video_length_hhmmss}`", inline = False)
                embed.add_field(name = '조회수', value=f"{_song_data['video_view_count']:,}", inline=True)
                embed.add_field(name = '게시자', value=f"{_song_data['video_uploader']}", inline=True)
                embed.set_thumbnail(url = f"{_song_data['video_thumbnail']}")
                await self.ctx.send(embed = embed)

                player = discord.FFmpegPCMAudio(URL, **ffmpeg_options)
                self.ctx.voice_client.play(player)

                try:
                    while self.ctx.voice_client.is_playing() or self.ctx.voice_client.is_paused():
                        # To avoid multiple players try to initiate their playing (already playing error - client exception),
                        # We need to make sure that the songs in the playlist are executed up to one at a time in order.
                        await asyncio.sleep(0.1)
            
                except TypeError:
                    # When user makes the bot leaves immediately while playing media,
                    # NoneType of voice_client exception raise, You may ignore, it doesn't care.
                    pass

                # delete the element that is being processed by the player
                # del music_queues[server_id][0]
                await self.delete_queue(0, False)
                # ^^^^ Don't let this command into the upper while statement

            else:
                await self.ctx.send(f"플레이리스트에 있는 모든 파일들이 재생되었거나, 아직 플레이리스트에 아무것도 등록되어 있지 않아서 지금 당장은 재생할 수 없어요. 새로운 것들을 다시 넣고 재생해주세요!")
                break

                pass


    async def pause_media(self):

        if self.ctx.author.voice is None or self.ctx.voice_client is None:
            await self.ctx.reply("음성채널에 봇과 함께 같이 있는지 확인해주세요!")
            return

        if self.ctx.voice_client.is_paused():
            # Media is not paused or not playing
            await self.ctx.reply("이미 일시정지되어 있거나 현재 무언가를 정지 가능한 상황이 아닙니다.")
        else:
            self.ctx.voice_client.pause()
            await self.ctx.reply("재생중이던 미디어를 일시정지했습니다.")

    async def resume_media(self):

        if self.ctx.author.voice is None or self.ctx.voice_client is None:
            await self.ctx.reply("음성채널에 봇과 함께 같이 있는지 확인해주세요!")
            return

        if self.ctx.voice_client.is_paused():
            # Media is now paused, so resume the play.
            self.ctx.voice_client.resume()
            await self.ctx.reply("정지한 미디어를 다시 재생합니다.")
        else:
            await self.ctx.reply("이미 재생 중이거나 현재 무언가를 다시 재생할 상황이 아닙니다.")

    async def skip_media(self):

        if self.ctx.author.voice is None or self.ctx.voice_client is None:
            await self.ctx.reply("음성채널에 봇과 함께 같이 있는지 확인해주세요!")
            return
        
        if self.ctx.voice_client.is_playing():
            self.ctx.voice_client.stop()
            await self.ctx.reply("재생하던 미디어를 중단하고 가능하면 다음 미디어로 넘어갑니다.")
        else:
            await self.ctx.reply("현재 미디어의 재생을 중단하고 넘어갈 수 있는 상황이 아닙니다.")


async def voice_channel_playlist(ctx, server_id, method_name, *args):

    # Manage instance of class VoiceChannelMusicPerServer
    # if the server requests some tasks about playing music in voice channel

    global active_voice_channal_class_dict

    # Create instance of class VoiceChannelMusicPerServer if there's nothing for the server (never created)
    server_voice_channel_class_name = f"VoiceChannelMusic_{server_id}"
    if server_voice_channel_class_name not in active_voice_channal_class_dict.keys():
        server_voice_channel_class = VoiceChannelMusicPerServer(ctx, server_id)
        active_voice_channal_class_dict[server_voice_channel_class_name] = server_voice_channel_class
        await ctx.reply("이 서버에서 사용되는 음악 플레이리스트가 아직 없어서 하나 만들었어요.")
    else:
        server_voice_channel_class = active_voice_channal_class_dict[server_voice_channel_class_name]

    return await getattr(server_voice_channel_class, method_name)(*args)