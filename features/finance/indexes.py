import requests
import time
import random
import os
import ast
import pickle
import discord
from ..convert_number_notation import get_korean_number_amount

class CustomUserAgentString:

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

class get_kr_finance_information:

    @staticmethod
    def fetch_overall_information():

        # to prevent excessive requests, store data as a JSON file that is valid for 60 seconds
        # kr_finance_raw_data_file_path = f"{os.getcwd()}/kr_index_raw.data.pickle"
        kr_finance_raw_data_file_path = f"./features/finance/indexes/kr_index_raw.data.pickle"

        if not os.path.isfile(kr_finance_raw_data_file_path) or not time.time() - os.path.getmtime(kr_finance_raw_data_file_path) < 60:
        
            request_url_list = { "overview"         : "https://api.finance.naver.com/service/mainSummary.naver",                                      # overview market
                                 "major_indexes"    : "https://polling.finance.naver.com/api/realtime?query=SERVICE_INDEX:KOSPI,KOSDAQ,KPI200" }      # major index
            headers = { "user-agent" : random.choice(CustomUserAgentString.user_agent_string_list) }

            kr_finance_raw_data = {}

            # annotation, url
            for key, value in request_url_list.items():
                response = requests.get(value, headers = headers)
                                                # Python uses "None" instead of "null"
                data = response.text.replace("null", "None")
                kr_finance_raw_data[key] = data

            with open(kr_finance_raw_data_file_path, 'wb') as file:
                pickle.dump(kr_finance_raw_data, file)
        

        with open(kr_finance_raw_data_file_path, 'rb') as file:
            kr_finance_data = pickle.load(file)

        return kr_finance_data


    @staticmethod
    def extract_data_by_criteria(criteria:str):

        kr_finance_data = get_kr_finance_information.fetch_overall_information()

        available_criterias = {
            # daily overall top ranking
            "top_trades"        : ["overview", "message", "result", "topItems", 0],
            "top_rise"          : ["overview", "message", "result", "topItems", 1],
            "top_fall"          : ["overview", "message", "result", "topItems", 2],
            "top_market_cap"    : ["overview", "message", "result", "topItems", 3],
            
            # daily specified ranking
            "group_top_list"    : ["overview", "message", "result", "groupTopList"],
            "theme_top_list"    : ["overview", "message", "result", "themeTopList"],

            # index ranking
            "daily_index_trend" : ["overview", "message", "result", "todayIndexDealTrendList"],     # buy/sell trend
            "daily_index_items" : ["overview", "message", "result", "todayIndexItemList"],          # rise/even/steady count in the index

            # index value
            "daily_index_stats" : ["major_indexes", "result", "areas"]                              # index stat with highly-abbreviated keys

        }

        if criteria not in available_criterias:
            print("Unavilable criteria")
            return

        # find multi-depth dictionary dynamically according to the given criteria
        result = kr_finance_data

        for search_option in available_criterias[criteria]:
            try:
                result = result[search_option]
            except TypeError:
                result = dict(ast.literal_eval(result))
                result = result[search_option]

        return result


    @staticmethod
    def get_index_overview(index:str):

        if index not in ["KOSPI", "KOSDAQ", "KPI200"]:
            print("Unavailable index")
            return
        
        daily_index_trend   = get_kr_finance_information.extract_data_by_criteria(criteria = "daily_index_trend")
        daily_index_items   = get_kr_finance_information.extract_data_by_criteria(criteria = "daily_index_items")
        daily_index_stats   = get_kr_finance_information.extract_data_by_criteria(criteria = "daily_index_stats")

        if index == "KOSPI":
            data_dict_index = 0
        elif index == "KOSDAQ":
            data_dict_index = 1
        else:       # KPI200
            data_dict_index = 2


        result = {
            "item_code"             : index,

            # index trends (unit : KRW)
            "personal_value"        : round(float(daily_index_trend[data_dict_index]["personalValue"]) * 100000000),
            "foreign_value"         : round(float(daily_index_trend[data_dict_index]["foreignValue"]) * 100000000),
            "institution_value"     : round(float(daily_index_trend[data_dict_index]["institutionalValue"]) * 100000000),

            # index statistics
            "market_open_close"     : daily_index_stats[0]["datas"][data_dict_index]["ms"],
            "current_value"         : int(daily_index_stats[0]["datas"][data_dict_index]["nv"]) / 100,
            "current_change_value"  : int(daily_index_stats[0]["datas"][data_dict_index]["cv"]) / 100,
            "current_change_rate"   : round(daily_index_stats[0]["datas"][data_dict_index]["cr"], 2),       # change rate (%)
            "daily_high_value"      : int(daily_index_stats[0]["datas"][data_dict_index]["hv"]) / 100,
            "daily_low_value"       : int(daily_index_stats[0]["datas"][data_dict_index]["lv"]) / 100,
            "acc_trading_volume"    : int(daily_index_stats[0]["datas"][data_dict_index]["aq"]) * 1000,
            "acc_trading_price"     : int(daily_index_stats[0]["datas"][data_dict_index]["aa"]) * 1000000,  # 1 = million won,
            "graph_image_url"      : f"https://ssl.pstatic.net/imgfinance/chart/main/{index}.png"
        }

        if index in ["KOSPI", "KOSDAQ"]:
            # They're not provided in case of KPI200 index overview.
            result.setdefault("upper_limit_count", daily_index_items[data_dict_index]["upperCnt"])
            result.setdefault("rise_count", daily_index_items[data_dict_index]["riseCnt"])
            result.setdefault("steady_count", daily_index_items[data_dict_index]["steadyCnt"])
            result.setdefault("fall_count", daily_index_items[data_dict_index]["fallCnt"])
            result.setdefault("lower_count", daily_index_items[data_dict_index]["lowerCnt"])

        return result

async def show_index_statistics(index_name:str):

    result = get_kr_finance_information.get_index_overview(index = index_name)

    embed = discord.Embed(title = f"{index_name}", color = 0x03C75A)
    embed.add_field(name = "개장 여부", value = f"`{result['market_open_close']}`", inline = True)
    embed.add_field(name = "체결가", value = f"**{result['current_value']}**", inline = True)
    embed.add_field(name = "변동", value = f"{result['current_change_value']} ({result['current_change_rate']} %)", inline = True)
    embed.add_field(name = "고가 / 저가", value = f"> 장중 최고 : {result['daily_high_value']}\n> 장중 최저 : {result['daily_low_value']}", inline = True)
    embed.add_field(name = "1일 거래 규모", value = f"> 거래 대금 : {get_korean_number_amount(result['acc_trading_price'])} 원\n> 거래량 ≈ {get_korean_number_amount(result['acc_trading_volume'])} 주", inline = False)
    embed.add_field(name = "투자자별 매매 동향", value = f"> 개인 : {get_korean_number_amount(result['personal_value'])} 원\n> 기관 : {get_korean_number_amount(result['institution_value'])} 원\n> 외국인 : {get_korean_number_amount(result['foreign_value'])} 원", inline = True)

    if index_name != "KPI200":
        embed.add_field(name = "등락 종목", value = f"⏫ × {result['upper_limit_count']} | 🔼 × {result['rise_count']} | ⏸ × {result['steady_count']} | 🔽 × {result['fall_count']} ⏬ × {result['lower_count']}", inline = False)

    embed.set_image(url = result['graph_image_url'])
    embed.set_footer(text = "과도한 요청을 방지하기 위하여 데이터는 실제와 최대 1분가량 차이가 나는 값일 수 있으며, 시장 거래가 휴장인 경우 가장 최근 개장 시점의 데이터를 불러옵니다. 모든 수치 데이터는 개장 시점부터 현재(장 마감시 그 시점까지)까지 집계된 값입니다. 기술상 한계로 KPI200 Index는 등락 종목 통계를 제공해드릴 수 없으므로 양해 바랍니다. 버튼이 작동하지 않으면 명령어를 다시 입력해 최신 정보를 받아보세요.")

    return embed


class IndexInfoMenu(discord.ui.View):
    def __init__(self, ctx):
        super().__init__()
        self.value = None
        self.ctx = ctx

    @discord.ui.button(label = "KOSPI", style = discord.ButtonStyle.grey)
    async def KOSPI(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = await show_index_statistics(index_name ="KOSPI")
        await interaction.response.edit_message(embed = embed)

    @discord.ui.button(label = "KOSDAQ", style = discord.ButtonStyle.grey)
    async def KOSDAQ(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = await show_index_statistics(index_name ="KOSDAQ")
        await interaction.response.edit_message(embed = embed)

    @discord.ui.button(label = "KPI200", style = discord.ButtonStyle.grey)
    async def KPI200(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = await show_index_statistics(index_name ="KPI200")
        await interaction.response.edit_message(embed = embed)
