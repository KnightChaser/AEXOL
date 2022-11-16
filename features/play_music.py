import discord
from youtube_dl import YoutubeDL
import datetime

players = {}
music_queues = {}

# def check_queue(id):
#     if queues[id] != []:
#         player = queues[id].pop(0)
#         players[id] = player
#         player.start()


async def add_queue(ctx, server_id, requested_url):

    # check whether requested url is for available Youtube Video
    try:
        with YoutubeDL() as ydl:
            ydl_extracted         = ydl.extract_info(requested_url, download = False)
            video_information     = {
                "video_url"         : ydl_extracted.get("url", None),
                "video_title"       : ydl_extracted.get("title", None),
                "video_duration"    : ydl_extracted.get("duration", None)
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

    local_playlist_string = ""

    try:
        local_playlist = music_queues[server_id]

        if local_playlist == None:
            local_playlist_string = "아직 아무것도 없어요..."
        else:
            for index, music_info in enumerate(local_playlist):
                index_number           = '{0: >4}'.format(index)
                video_length_hhmmss    = str(datetime.timedelta(seconds = music_info['video_duration']))
                local_playlist_string += f"#{index_number} : {music_info['video_title']} ({video_length_hhmmss})\n"
    except KeyError:
        # if there is nothing on music_queues(0 items) and someone tries to show the playlist at that moment,
        # the keyerror will be occured because the key is NOT vaild for the playlist WITH NOTHING.
        local_playlist_string = "아직 아무것도 없어요..."

    embed = discord.Embed(title = f"💽 재생목록", color = 0x00FFDB)
    embed.add_field(name = f"현재 서버 : {server_name}", value = f"```{local_playlist_string}```", inline = False)

    await ctx.reply(embed = embed)

async def delete_element_in_queue(ctx, server_id, index):
    global music_queues
    
    # A user requests to delete everything in the current queue
    if index == "*":
        music_queues[server_id] = []
        await ctx.reply("재생목록에 있는 내용을 모두 지웠어요.")
    else:
        try:
            target_title = music_queues[server_id][index]['video_title']
            music_queues[server_id].pop(index)

            await ctx.reply(f"[#{index}] **\"{target_title}\"**을 재생목록에서 삭제했어요.")
        except IndexError:
            await ctx.reply("요청하신 번호에 해당하는 내용이 재생목록에 없어요. 한번 다시 확인해주세요!")