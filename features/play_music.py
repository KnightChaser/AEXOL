import discord
import youtube_dl
import datetime
import asyncio

players = {}
music_queues = {}

async def add_queue(ctx, server_id, requested_url):

    # playlist_detector_in_url = ['&start_radio', '&list', '&index']
    allowable_youtube_link_detector = ['https://www.youtube.com/watch?v=', 'https://youtu.be/']
    if not requested_url.startswith(tuple(allowable_youtube_link_detector)) or "&start_radio" in requested_url or "&list" in requested_url or "&index" in requested_url:
        # when user gives playlist or station link of Youtube to play via this bot,
        # ffmpeg that is belonged to this tries to download everything in ths playlist so the task consumes so much time
        # and that's unexpected. so URL for playlist and station is blocked by these techincal issues.
        await ctx.reply(f"죄송해요! YouTube 영상 링크는 반드시 `https://www.youtube.com/watch?v=` 또는 `https://youtu.be/`로 시작해야 하며 YouTube Station 또는 플레이리스트 링크는 기술상 제약으로 인해 허용되지 않습니다.")
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
        await ctx.reply(f"유효하지 않은 Youtube 동영상 링크인 것 같아요.")
        return

    global music_queues

    if server_id not in music_queues.keys():
        # create music queues for the servers without current music queue
        music_queues[server_id] = []
        await ctx.send("이 서버에서 사용되는 음악 플레이리스트가 없어서 하나 만들었어요.")
    music_queues[server_id].append(video_information)

    video_length_hhmmss    = str(datetime.timedelta(seconds = video_information['video_duration']))
    await ctx.send(f"💽 [**{video_information['video_title']}**]를 플레이리스트에 추가했어요. (재생 시간 : {video_length_hhmmss})")

async def show_queue(ctx, server_id):
    global music_queues
    server_name = ctx.guild.name

    local_playlist_string = "아직 아무것도 없어요..."           # <--- default message (when nothing inside the playlist)

    try:
        local_playlist = music_queues[server_id]

        if local_playlist == None:
            pass
            # local_playlist_string = "아직 아무것도 없어요..."
        else:
            local_playlist_string = ""
            for index, music_info in enumerate(local_playlist):
                index_number           = '{0: >4}'.format(index)
                video_length_hhmmss    = str(datetime.timedelta(seconds = music_info['video_duration']))
                local_playlist_string += f"#{index_number} : {music_info['video_title']} ({video_length_hhmmss})\n"
    except KeyError:
        # if there is nothing on music_queues(0 items) and someone tries to show the playlist at that moment,
        # the keyerror will be occured because the key is NOT vaild for the playlist WITH NOTHING.
        pass
        # local_playlist_string = "아직 아무것도 없어요..."

    embed = discord.Embed(title = f"💽 재생목록", color = 0x00FFDB)
    embed.add_field(name = f"현재 서버 : {server_name}", value = f"```{local_playlist_string}```", inline = False)
    embed.set_footer(text = "등록된 순서에 따라, #0 부터 노래가 순서대로 재생됩니다.")

    await ctx.reply(embed = embed)

async def delete_element_in_queue(ctx, server_id, index, notify):
    global music_queues
    
    # A user requests to delete everything in the current queue
    if index == "*":
        music_queues[server_id] = []
        await ctx.reply("재생목록에 있는 내용을 모두 지웠어요.")
    else:
        try:
            target_title = music_queues[server_id][index]['video_title']
            music_queues[server_id].pop(index)
            if notify == True:
                # if user deleted the element manually, we let the user know
                await ctx.reply(f"[#{index}] **\"{target_title}\"**을 재생목록에서 삭제했어요.")
            else:
                # if program deleted the element automatically, we don't need to let the user know
                pass
        except IndexError:
            await ctx.reply("요청하신 번호에 해당하는 내용이 재생목록에 없어요. 한번 다시 확인해주세요!")

async def play_queue(ctx, server_id):
# async def play_queue(ctx, server_id, requested_url):
    global music_queues

    if ctx.author.voice == None:
        # Author is not connected to the voice channel
        await ctx.reply("음성채널에 먼저 들어와 주세요.")
        return

    if ctx.voice_client == None:
        # Bot is not connected to the voice channel
        await ctx.reply("음성채널에 아직 있는 것 같지 않아요. 저를 음성채널에 먼저 들여보내 주세요!")
        return

    ffmpeg_options = {
        'options': '-vn', 
        "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
    }

    while True:

        if music_queues[server_id] != []:
            # play until the playlist has nothing
            _song_data = music_queues[server_id][0]

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
            await ctx.send(embed = embed)

            player = discord.FFmpegPCMAudio(URL, **ffmpeg_options)
            ctx.voice_client.play(player)

            try:
                while ctx.voice_client.is_playing() or ctx.voice_client.is_paused():
                    # To avoid multiple players try to initiate their playing (already playing error - client exception),
                    # We need to make sure that the songs in the playlist are executed up to one at a time in order.
                    await asyncio.sleep(0.1)
            except AttributeError:
                # when you make the bot leave the voice channel, conditional statement in while
                # occurs unexpected but ignorable exceptions and ctx messages. You may ignore, it doesn't care.
                pass

            # delete the element that is being processed by the player
            # del music_queues[server_id][0]
            await delete_element_in_queue(ctx, server_id, 0, False)
            # ^^^^ Don't let this command into the upper while statement

        else:
            await ctx.send(f"플레이리스트에 있는 모든 파일들이 재생되었거나, 아직 플레이리스트에 아무것도 등록되어 있지 않아서 지금 당장은 재생할 수 없어요. 새로운 것들을 다시 넣고 재생해주세요!")
            break

async def pause(ctx, server_id):

    if ctx.voice_client.is_paused():
        # Media is not paused or not playing
        await ctx.reply("이미 일시정지되어 있거나 현재 무언가를 정지 가능한 상황이 아닙니다.")
    else:
        ctx.voice_client.pause()
        await ctx.reply("재생중이던 미디어를 일시정지했습니다.")

async def resume(ctx, server_id):

    if ctx.voice_client.is_paused():
        # Media is now paused, so resume the play.
        ctx.voice_client.resume()
        await ctx.reply("정지한 미디어를 다시 재생합니다.")
    else:
        await ctx.reply("이미 재생 중이거나 현재 무언가를 다시 재생할 상황이 아닙니다.")

async def skip(ctx, server_id):
    
    if ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        await ctx.reply("재생하던 미디어를 중단하고 가능하면 다음 미디어로 넘어갑니다.")
    else:
        await ctx.reply("현재 미디어의 재생을 중단하고 넘어갈 수 있는 상황이 아닙니다.")