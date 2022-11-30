import discord
from discord import Option
from discord.ext import commands
import requests
from bs4 import BeautifulSoup
import time
import re
import random
from components.convert_number_notations import ConvertNumberNotations as convert_number_notations

class Google(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    google = discord.SlashCommandGroup(name = "google", description = "구글 검색")

    @google.command(description = "인덱스 검색(빠르게 찾기)")
    async def index(self,
                    ctx,
                    search_word: Option(str, "검색어")):

        result_as_embed = await get_google_search_index(ctx = ctx, keyword = search_word)
        await ctx.respond(embed = result_as_embed)


def setup(bot):
    bot.add_cog(Google(bot))

#########################################################################

class GoogleParsingConst:

    index_name_class_name = "LC20lb MBeuO DKV0Md"
    index_url_class_name  = "iUh30 qLRx3b tjvcx"
    html_tag_del_regex    = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    html_entity_del_regex = re.compile('&(?:[a-z\d]+|#\d+|#x[a-f\d]+)')

    user_agent_string_list = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64; rv:106.0) Gecko/20100101 Firefox/106.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:106.0) Gecko/20100101 Firefox/106.0',
        'Mozilla/5.0 (Windows NT 10.0; rv:106.0) Gecko/20100101 Firefox/106.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.52',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.35'
    ]


def process_google_search_index(keyword):

    if keyword == None:
        return False

    start_time = time.time()

    try:
        url = f"https://www.google.com/search?q={keyword}"
        headers = {"user-agent" : random.choice(GoogleParsingConst.user_agent_string_list) }
        res = requests.get(url, headers = headers)
        soup = BeautifulSoup(res.text, 'html.parser')
    except Exception as e:
        return (False, e)

    result_stat = soup.select_one("#result-stats").text
    result_count = (lambda data: int(data.split(' ')[2].replace('개', '').replace(',', '')))(result_stat)                       # how many results?
    result_time  = (lambda data: float(data.split(' ')[3].replace('(', '').replace(')', '').replace('초', '')))(result_stat)    # how much time Google spent?
    
    result_index_name_list   = (lambda data: data.find_all("h3", {"class" : GoogleParsingConst.index_name_class_name}))(soup)
    result_index_url_list    = (lambda data: data.find_all("cite", {"class" : GoogleParsingConst.index_url_class_name}))(soup)
    
    # making results as a dictionary
    result = {}
    result['search_keyword'] = keyword
    result['search_result'] = result_count
    result['search_time'] = result_time
    result['index'] = {}

    _seq = 0

    for result_index_name, result_index_url in zip(result_index_name_list, result_index_url_list):

        result_index_name = str(result_index_name)
        result_index_url  = str(result_index_url)

        if _seq >= 10:       # only TOP 10 result will be the maximum limit
            break

        result_index_name = re.sub(GoogleParsingConst.html_tag_del_regex, '', result_index_name)
        result_index_name = re.sub(GoogleParsingConst.html_entity_del_regex, '', result_index_name)

        result_index_url  = re.sub(GoogleParsingConst.html_tag_del_regex, '', result_index_url)
        result_index_url  = re.sub(GoogleParsingConst.html_entity_del_regex, '', result_index_url)
        result_index_url  = (lambda data: data.replace("›", '/').replace(' ', ''))(result_index_url)    # Google splits its url as their own way,
                                                                                                        # "/" to "›" (U+203a) (* NOt ">")
        
        result['index'][_seq] = {
            'index_name' : result_index_name,
            'index_url'  : result_index_url
        }

        _seq += 1

    finish_time = time.time()
    processing_time = finish_time - start_time

    result['processing_time'] = processing_time

    return result

async def get_google_search_index(ctx, keyword):

    result = process_google_search_index(keyword)

    if type(result) is tuple:
        await ctx.reply(f"검색 처리 과정 중에 에러가 발생한 것 같아요. ...`{result[1]}`")
        return

    # all process has done successfully
    embed = discord.Embed(title = f"🔍 구글 검색 : `{result['search_keyword']}`", color = 0x00FFDB)
    embed.add_field(name = "검색 통계", value = f"📟검색 결과 개수 : ≈ **{convert_number_notations.get_korean_number_amount(result['search_result'])}** 개\n⏲️검색 시간 : **{round(result['search_time'], 3)}초**", inline = False)

    index_show_text = ""
    for _seq in result['index']:
        _data = result['index'][_seq]

        data_text = f"**#{_seq + 1}** : "
        data_text += f"[{_data['index_name']}]({_data['index_url']})\n"

        if len(index_show_text) + len(data_text) >= 1024:
            # reached discord embed field value char limit
            break
        index_show_text += data_text
        

    embed.add_field(name = "상위 검색 결과", value = f"{index_show_text}")
    embed.set_footer(text = f"프로세스 처리 시간 : {round(result['processing_time'], 3)}초 | 가능한 최대 상위 10개 결과만 보여집니다.")
    return embed