import requests
import mplfinance
import pandas
import time
import json
import os
import ast
import io
import discord


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
            symbol = markets.replace('KRW-','').replace('BTC-','')

            if "KRW-" in markets:
                fiat_currency = "KRW"
                fiat_symbol = "₩"
            elif "BTC-" in markets:
                fiat_currency = "BTC"
                fiat_symbol = "₿"

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
    if float(data['change_rate']) * 100 >= 40:
        change_emoji = '🔥'
        change_comment = '폭등'
    elif float(data['change_rate']) * 100 >= 20:
        change_emoji = '⏫'
        change_comment = '급등'
    elif float(data['change_rate']) * 100 > 0:
        change_emoji = '🔼'
        change_comment = '상승'
    elif float(data['change_rate']) == 0 or data['change'] == "EVEN":      # for potential floating point issue, one more condition to clarify
        change_emoji = '⏸'
        change_comment = '보합'
    elif float(data['change_rate']) * 100 >= -20:
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
        'opening_price'         : format(data['opening_price'], ','),
        'high_price'            : format(data['high_price'], ','),
        'low_price'             : format(data['low_price'], ','),
        'trade_price'           : format(data['trade_price'], ','),
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
        url = f"https://api.upbit.com/v1/candles/minutes/{minutes}?market={markets}&count=100"
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
                        title = f"\n\n\n\n\n\n\n\n{' ' * 60}{markets}",
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

    embed.add_field(name = "현재 가격(거래가)", value = f"**{fiat_symbol} {market_ticker_information['trade_price']}**", inline = True)
    embed.add_field(name = "52주 고저", value = f"""고가 : {fiat_symbol} {market_ticker_information['highest_52_week_price']}
                                                    저가 : {fiat_symbol} {market_ticker_information['lowest_52_week_price']}""")
    embed.add_field(name = "24시간 가격 변동폭", value = f"""시가 : {fiat_symbol} {market_ticker_information['opening_price']}
                                                            고가 : {fiat_symbol} {market_ticker_information['high_price']}
                                                            저가 : {fiat_symbol} {market_ticker_information['low_price']}""", inline = True)
    embed.add_field(name = "24시간 변동", value = f"**{fiat_symbol} {market_ticker_information['change_rate_price']}**\n{market_ticker_information['change_rate_percent']} % {market_ticker_information['change_emoji']}", inline = True)
    embed.add_field(name = "24시간 거래량", value = f"≈ {fiat_symbol} {market_ticker_information['acc_trade_price_24h']} (≈ {market_ticker_information['acc_trade_volume_24h']} {market_symbol})", inline = False)

    candle_chart_picture = discord.File(market_candle_chart, filename = "candlechart.png")
    embed.set_image(url = f"attachment://candlechart.png")
    embed.set_footer(text = f"Upbit 제공 | 업데이트 시각 : {market_ticker_information['trade_kst_format']}")

    # await ctx.reply(embed = embed)
    await ctx.channel.send(file = candle_chart_picture, embed = embed)        

# print(get_crypto_info("KRW-IQ"))