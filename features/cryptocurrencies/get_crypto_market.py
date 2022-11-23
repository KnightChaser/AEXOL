import requests
import mplfinance
import pandas
import time
import json
import os
import ast
import discord
import matplotlib.font_manager as fm
from table2ascii import *

# number formatter for chart, enhances visibilities
def add_comma_formatter(number, pos):
    if number >= 1000:
        return '{0:,}'.format(round(number))            # to avoid attach unnecessary comma
    else:
        return round(number, 10)

# first, check whether the requested market code is available in Upbit exchange
def check_available_market_codes(markets:str):

    # availability_list_file_path = "./available_market_codes.json"
    availability_list_file_path = "./features/cryptocurrencies/available_market_codes.json"

    if not os.path.isfile(availability_list_file_path) or not time.time() - os.path.getmtime(availability_list_file_path) < 600:
        # if the list file is not exist or
        # the file has been updated more than 10 minutes(600 sec.) ago
        url = "https://api.upbit.com/v1/market/all?isDetails=true"
        headers = {"accept": "application/json"}
        response = requests.get(url, headers=headers)
        raw_data = json.dumps(response.text)

        file = open(availability_list_file_path, 'w')

        # make dictionary for python form
        file.write(raw_data)

        file.close()

    with open(availability_list_file_path) as file:
        json_object = json.load(file)
        market_availability_dict = ast.literal_eval(json_object)

    result = False
        
    for _data in market_availability_dict:
        if _data["market"] == markets:
            symbol = markets.replace('KRW-','').replace('BTC-','').replace('USDT-','')

            if "KRW-" in markets:
                fiat_currency = "KRW"
                fiat_symbol = "₩"
            elif "BTC-" in markets:
                fiat_currency = "BTC"
                fiat_symbol = "₿"
            elif "USDT-" in markets:
                fiat_currency = "USDT"
                fiat_symbol = "₮"

            result = {
                "market_code"       : markets,
                "symbol"            : symbol,
                "korean_name"       : _data["korean_name"],
                "english_name"      : _data["english_name"],
                "market_icon_url"   : f"https://static.upbit.com/logos/{symbol}.png",
                "market_warning"    : _data["market_warning"],
                "fiat_currency"     : fiat_currency,
                "fiat_symbol"       : fiat_symbol
            }
            break

    return result
    
# second, get ticker information (quote), extract informations like current value
def get_crypto_ticker(markets:str):

    url = f"https://api.upbit.com/v1/ticker?markets={markets}"

    headers = {"accept" : "application/json"}

    response = requests.get(url, headers = headers)

    if "Code not found" in response.text:
        return "code not found"

    # data = ast.literal_eval(response.text)
    data = json.loads(response.text)
    data = data[0]

    # set some visual emojis for Discord embed
    if float(data['signed_change_rate']) * 100 >= 40:
        change_emoji = '🔥'
        change_comment = '폭등'
    elif float(data['signed_change_rate']) * 100 >= 20:
        change_emoji = '⏫'
        change_comment = '급등'
    elif float(data['signed_change_rate']) * 100 > 0:
        change_emoji = '🔼'
        change_comment = '상승'
    elif float(data['signed_change_rate']) == 0 or data['change'] == "EVEN":      # for potential floating point issue, one more condition to clarify
        change_emoji = '⏸'
        change_comment = '보합'
    elif float(data['signed_change_rate']) * 100 >= -20:
        change_emoji = '🔽'
        change_comment = '하락'
    else:
        change_emoji = '⏬'
        change_comment = '급락'

    if "KRW-" in data['market']:
        formatted_acc_trade_price_24h = format(round(data['acc_trade_price_24h']), ',')
    else:
        formatted_acc_trade_price_24h = format(round(data['acc_trade_price_24h'], 3), ',')

    result = {
        'market'                : data['market'],
        'opening_price'         : format(round(data['opening_price'], 6), ','),
        'high_price'            : format(round(data['high_price'], 6), ','),
        'low_price'             : format(round(data['low_price'], 6), ','),
        'trade_price'           : format(round(data['trade_price'], 6), ','),
        'change'                : data['change'],
        'change_comment'        : change_comment,
        'change_emoji'          : change_emoji,
        'change_rate_percent'   : round(data['signed_change_rate'] * 100, 2),
        'change_rate_price'     : format(data['signed_change_price'], ','),
        'acc_trade_price_24h'   : formatted_acc_trade_price_24h,
        'acc_trade_volume_24h'  : format(round(data['acc_trade_volume_24h'], 2), ','),
        'highest_52_week_price' : format(data['highest_52_week_price'], ','),
        'lowest_52_week_price'  : format(data['lowest_52_week_price'], ','),
        'trade_kst_format'      : f"{data['trade_date_kst']} {data['trade_time_kst']}"
    }

    return result

# third, draw a graph
def get_crypto_candle_chart(markets:str, minutes:int):

    try:

        # retrive required recent candlestick informations
        url = f"https://api.upbit.com/v1/candles/minutes/{minutes}?market={markets}&count=150"
        headers = {"accept": "application/json"}
        response = requests.get(url, headers=headers)
        raw_json_data = response.text

        data = pandas.read_json(raw_json_data)
        data = data.drop(['market', 'candle_date_time_utc', 'candle_acc_trade_volume', 'unit'], axis = "columns")
        data = data[['candle_date_time_kst', 'opening_price', 'high_price', 'low_price', 'trade_price', 'candle_acc_trade_price']]
        data.index = pandas.to_datetime(data['candle_date_time_kst'])
        data.columns = ['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume']
        data = data.iloc[::-1]                                                # to show chart with time order


        candle_chart_color = mplfinance.make_marketcolors(
                                up = '#089981', down = '#F23645',             # candle tick color
                                wick = {                                      # candle wick color
                                    'up' : '#089981',
                                    'down' : '#F23645'
                                },
                                edge = {
                                    'up' : '#089981',
                                    'down' : '#F23645'
                                },
                                volume = '#808080'
                            )

        # custom font setting
        fm.fontManager.addfont("asset/font/Consolas.ttf")
        rcpdict = { 'font.family' : ['Consolas'] }

        candle_chart_style = mplfinance.make_mpf_style(
                                gridcolor = '#F2F3F3',
                                gridstyle = 'dashed',
                                marketcolors = candle_chart_color,
                                rc = rcpdict
                            )

        chart_filedir  = "./features/cryptocurrencies/figure"       # POV : the location of bot.py which runs these code

        if not os.path.isdir(chart_filedir):
            os.mkdir(chart_filedir)

        # chart_filename = f"{chart_filedir}/cryptochart-upbit-{int(time.time())}-{markets}.png"
        chart_filename = f"{chart_filedir}/candlestick_chart.png"            # to prevent too much file generation

        fig, axlist = mplfinance.plot(
                        data,
                        type = "candle",
                        volume = True,
                        title = f"\n\n{markets}@UpBit ({minutes}minutes/candle)",
                        style = candle_chart_style,
                        ylabel = "Price",
                        ylabel_lower = "Volume (KRW)",
                        xlabel = "Time in KST(UTC+09:00)",
                        returnfig = True,
                        # savefig = f"{filename}"
                    )

        axlist[2].set_ylabel("Price")
        axlist[2].set_ylabel("Volume")

        axlist[0].yaxis.set_major_formatter(add_comma_formatter)
        # axlist[0].yaxis.get_major_formatter().set_scientific(False)

        axlist[2].yaxis.set_major_formatter(add_comma_formatter)
        # axlist[2].yaxis.get_major_formatter().set_scientific(False)

        fig.savefig(chart_filename)

        # mplfinance.show()

        return chart_filename

    except Exception as err:

        raise(err)


async def get_crypto_info(ctx, markets:str):
# def get_crypto_info(minutes:int, markets:str):            # when you need to adjust minutes of the chart dynamically


    market_availability = check_available_market_codes(markets)

    if market_availability == False:
        # Invalid market code request. Terminal further processes
        await ctx.reply(f"입력하신 마켓 코드는 현재 데이터 제공업체인 **업비트(Upbit)** 거래소에서 지원하지 않습니다.")
        return
    
    market_ticker_information = get_crypto_ticker(markets)
    market_candle_chart       = get_crypto_candle_chart(markets, minutes = 3)       # By default, draw 3-minute candlestick chart

    market_symbol = market_availability['symbol']
    fiat_currency = market_availability['fiat_currency']
    fiat_symbol   = market_availability['fiat_symbol']


    embed = discord.Embed(title = f"🔍 실시간 암호화폐 시세 : **{market_symbol}**({market_availability['korean_name']})",  color = 0x00FFDB)
    embed.set_author(name = f"{market_availability['market_code']}", icon_url = f"{market_availability['market_icon_url']}")
    # embed.add_field(name = "영문 이름", value = f"{market_availability['english_name']}", inline = True)
    embed.add_field(name = "거래 통화", value = f"**{fiat_currency}**({fiat_symbol})", inline = True)

    if market_availability['market_warning'] == "NONE":
        market_warning_sign = "해당사항 없음 ✅"
    else:
        market_warning_sign = "투자 주의 🚧"
    embed.add_field(name = "유의 종목 여부", value = f"{market_warning_sign}", inline = True)

    embed.add_field(name = "현재 가격(거래가)", value = f"**{fiat_symbol} {market_ticker_information['trade_price']}**", inline = True)
    embed.add_field(name = "24시간 변동", value = f"**{fiat_symbol} {market_ticker_information['change_rate_price']}** ({market_ticker_information['change_rate_percent']} % {market_ticker_information['change_emoji']})", inline = True)
    embed.add_field(name = "52주 고저", value = f"""고가 : {fiat_symbol} {market_ticker_information['highest_52_week_price']}
                                                    저가 : {fiat_symbol} {market_ticker_information['lowest_52_week_price']}""")
    embed.add_field(name = "24시간 가격 변동폭(시가/고가/저가)", value = f"{fiat_symbol} {market_ticker_information['opening_price']} / {fiat_symbol} {market_ticker_information['high_price']} / {fiat_symbol} {market_ticker_information['low_price']}", inline = False)
    embed.add_field(name = "24시간 거래량", value = f"**{fiat_symbol}** {market_ticker_information['acc_trade_price_24h']} **≈** {market_ticker_information['acc_trade_volume_24h']} **{market_symbol}**", inline = False)

    candle_chart_picture = discord.File(market_candle_chart, filename = "candlechart.png")
    embed.set_image(url = f"attachment://candlechart.png")
    embed.set_footer(text = f"Upbit 제공 | 업데이트 시각 : {market_ticker_information['trade_kst_format']}")

    await ctx.channel.send(file = candle_chart_picture, embed = embed)        


# get sorted crypto market information by a specific criteria
# def get_crypto_ranking_by(criteria:str, market:str, order:str, rank_cut:int):
async def get_crypto_ranking_by(ctx, market:str, criteria:str, order:str):

    # manually set
    rank_cut = 20

    # to adjust upbit API spec
    if criteria == "change_price":
        criteria = "signed_change_price"
    elif criteria == "change_rate":
        criteria = "signed_change_rate"

    available_criterias_to_sort = {
        "opening_price"         : "시가",
        "high_price"            : "고가",
        "low_price"             : "저가",
        "trade_price"           : "현재가",
        "prev_closing_price"    : "전일 종가 (UTC 0시 기준)",
        "signed_change_price"   : "시세 변화액 (24시간)",
        "signed_change_rate"    : "시세 변화율 (24시간)",
        "acc_trade_price"       : "누적 거래대금 (UTC 0시 기준)",
        "acc_trade_price_24h"   : "누적 거래대금 (24시간)"
    }

    available_market_symbols = {
        "KRW" : {
            "fiat_currency" : "KRW",
            "fiat_symbol" : "₩"
        },
        "BTC" : {
            "fiat_currency" : "BTC",
            "fiat_symbol" : "₿"
        },
        "USDT" : {
            "fiat_currency" : "USDT",
            "fiat_symbol" : "₮"
        }
    }

    sorted_func_order = {
        "ascending"  : False,
        "descending" : True
    }

    headers = {"accept" : "application/json"}

    if criteria not in available_criterias_to_sort:
        raise("Unavailable criteria")

    if market not in available_market_symbols:
        raise("Unavailable market")

    if order not in sorted_func_order:
        raise("Unavailable sort function order direction")

    ### Just get market code ### 
    market_code_api_url = "https://api.upbit.com/v1/market/all?isDetails=false"
    market_code_raw_data = json.loads(requests.get(market_code_api_url, headers = headers).text)
    
    ticker_request_url = "https://api.upbit.com/v1/ticker?markets="
    for _data in market_code_raw_data:
        if f"{market}-" in _data['market']:
            ticker_request_url += f"{_data['market']},"
    ticker_request_url = ticker_request_url[:-1]                      # delete unnecessary ","
    ###

    ticker_raw_data = json.loads(requests.get(url = ticker_request_url, headers = headers).text)
    
    ticker_ranking_data = {}

    for _data in ticker_raw_data:
        ticker_ranking_data.setdefault(_data["market"])
        ticker_ranking_data[_data["market"]] = {
            criteria : _data[criteria]
        }

    # print(ticker_ranking_data.items())
    ticker_ranking_data = sorted(ticker_ranking_data.items(), key = lambda x: x[1][criteria], reverse = sorted_func_order[order])

    # pack the result to make the table as a result
    _seq = 1
    result_table_body_list = []
    for _data in ticker_ranking_data:
        if _seq > rank_cut:
            break

        # appropriate rounding and commas for numeric data
        numeric_data = _data[1][criteria]
        market_symbol = _data[0].replace("KRW-","").replace("BTC-","").replace("USDT-","")
        if criteria in ["acc_trade_price", "acc_trade_price_24h"]:
            numeric_data = f"{available_market_symbols[market]['fiat_symbol']} {format(round(numeric_data), ',')}"
        elif criteria == "signed_change_rate":
            numeric_data *= 100
            numeric_data = f"{format(round(numeric_data, 2), ',.2f')} %"
        elif criteria in ["opening_price", "high_price", "low_price", "trade_price", "prev_closing_price", "change_price"]:
            numeric_data = f"{available_market_symbols[market]['fiat_symbol']} {format(numeric_data, ',')}"

        result_table_body_list.append([f"{_seq}", f"{market_symbol}", f"{numeric_data}"])
        _seq += 1

    table_output = table2ascii(
        header              = ["#", "market", "value"],
        body                = result_table_body_list,
        style               = PresetStyle.ascii_compact,
        first_col_heading   = True,
        cell_padding        = 3,
        alignments          = [Alignment.RIGHT] + [Alignment.CENTER] + [Alignment.RIGHT] 
    )

                    #  |--- coin icon
    message_output = f"🪙 **암호화폐 통계** | **마켓** : {market}({available_market_symbols[market]['fiat_symbol']}) | **정렬** : {available_criterias_to_sort[criteria]}"
    message_output += f"```\n{table_output}\n```"      # for discord messaging
    message_output += "자료제공 : 업비트"

    await ctx.reply(message_output)