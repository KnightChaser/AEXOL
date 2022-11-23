supported_commands = {
    "change_status"   : {
        "description" : "봇의 상태를 바꿉니다",
        "usage"       : "axl! change_status [online|offline|idle|do_not_disturb|invisible]",
        "example"     : "axl! change_status online",
        "privilege"   : "administrator"
    },
    "crypto"          : {
        "description" : "업비트(Upbit) 거래소의 암호화폐 시세와 최근 차트(3분봉 캔들차트 + 거래량) 또는 원하는 기준에 따라 정렬된 상위 통계를 실시간으로 제공합니다.",
        "usage"       : "axl! crypto [market|rank]\n"
                      + "├axl! crypto market [market_code]\n"
                      + "└axl! crypto rank [fiat_currency] [sort_criteria] [sort_direction]",
        "example"     : "axl! crypto market KRW-BTC\n"
                      + "axl! crypto rank KRW acc_trade_price_24h descending",
        "privilege"   : "everyone",
        "detailed_descriptions" : {
            0 : {
                "title"     : "`axl! crypto market [...]`",
                "content"   : "`[market_code]` : 종목 코드 "
                            + "업비트 API 표준을 사용합니다. `[fiat_currency]-[cryptocurrency]` 형태를 사용하면 되며, 예를 들어 KRW(원화)로 거래되는 BTC(비트코인)에 대해 조회하고 싶을때는 마켓 코드로 `KRW-BTC`를 사용하세요."
            },
            1 : {
                "title"     : "`axl! crypto rank [...]`",
                "content"   : "`[fiat_currency]` : 거래 통화 (`KRW|BTC|USDT`)\n"
                            + "`[sort_criteria]` : 정렬 기준 (`opening_price|high_price|low_price|trade_price|prev_closing_price|signed_change_price|signed_change_rate|acc_trade_price|acc_trade_price_24h`)\n"
                            + "`[sort_direction]` : 기준에 따라 정렬된 값의 순서(오름차순/내림차순) (`ascending|descending`)\n"

            },
            2 : {
                "title"     : "지원되는 종목 확인하기",
                "content"   : "`https://api.upbit.com/v1/market/all?isDetails=true`에서 JSON 형태로, 또는 업비트(Upbit) 거래소에서 확인해 볼 수 있습니다. 원칙상 원화(KRW), 비트코인(BTC), 달러테더(USDT) 마켓 모두를 지원합니다."
            }
        },
    },
    "time"            : {
        "description" : "현재 시간을 초 단위로 알려줍니다. 단, 시간은 서버가 위치한 한국시(한국표준시, KST)를 기준으로 합니다.",
        "usage"       : "axl! time",
        "example"     : "axl! time",
        "privilege"   : "everyone"
    },
    "google"          : {
        "description" : "제시한 키워드에 대한 구글 검색을 수행하여 간단한 통계와 상위 검색 결과를 정리해서 가져옵니다. 키워드에 공백이 들어간 경우 `\"python 3\"`와 같이 양변에 따옴표를 통해 키워드를 감싸 검색할 수 있습니다.",
        "usage"       : "axl! google [keyword]",
        "example"     : "axl! google \"about python\"",
        "privilege"   : "everyone"
    },
    "hello"           : {
        "description" : "봇에게 인사를 시킵니다.",
        "usage"       : "axl! hello",
        "example"     : "axl! hello",
        "privilege"   : "everyone"
    },
    "help"            : {
        "description" : "도움말을 출력합니다.",
        "usage"       : "axl! help [command(without \"!\")]",
        "example"     : "axl! help crypto",
        "privilege"   : "everyone"
    },
    "ping"            : {
        "description" : "원하는 타겟의 네트워크 연결 상태를 확인합니다. (ICMP ECHO/REPLY)",
        "usage"       : "axl! ping [target_ip_address|target_url]",
        "example"     : "axl! ping 8.8.8.8",
        "privilege"   : "everyone"
    },
    "voice_channel"   : {
        "description" : "봇을 음성 채널에 초대시키거나 나가도록 합니다. 이때, 초대하기 전 먼저 원하는 음성 채널에 사용자가 위치해야 합니다. 나갈 때는 음성 채널에 꼭 있지 않아도 됩니다.",
        "usage"       : "axl! voice_channel [join|leave]",
        "example"     : "axl! voice_channel join\n"
                      + "axl! voice_channel playlist add youtube.com/example_url\n"
                      + "axl! voice_channel playlist delete 3\n"
                      + "axl! voice_channel playlist resume",
        "privilege"   : "everone",
        "detailed_descriptions" : {
            0 : {
                "title"     : "🎵 추가 : YouTube 음악 재생하기",
                "content"   : "이 봇의 `voice_channel` 명령어를 사용해서 YouTube의 음악을 플레이리스트에 담고, 재생하고, 삭제하거나, 건너뛰는 등의 경험을 해 보실 수 있습니다. 아래 명령어를 참고하시고, 반드시 명령어는 한 번에 한 줄 씩만 넣어주세요."
            },
            1 : {
                "title"     : "💽 플레이리스트 만들기",
                "content"   : """
                플레이리스트에 YouTube 영상 링크를 넣고, 재생하실 수 있습니다.
                `axl! voice_channel playlist show` : 리스트 조회
                `axl! voice_channel playlist add [youtube_url]` : 유튜브 음악 영상 리스트에 추가
                `axl! voice_channel playlist delete [number]` : 리스트의 [특정 번호] 음악 삭제 (전부 삭제하고 싶다면 번호 대신 *을 입력하세요.)
                `axl! voice_channel playlist play` : 리스트의 노래를 순서대로 재생
                `axl! voice_channel playlist pause` : 재생되는 노래를 일시 정지
                `axl! voice_channel playlist resume` : 일시 정지된 노래를 이어 재생
                `axl! voice_channel playlist skip` : 다음 노래로 즉시 이동
                """
            },
            2 : {
                "title"     : "📜 참고 사항",
                "content"   : """
                봇과 함께 음성 채널에 들어온 다음 명령을 실행하세요.
                노래 재생은 리스트에 노래를 담고 나서 할 수 있습니다.
                노래 재생 전 다운로드로 인해 시간 지연이 있을 수 있습니다.
                아직 베타 기능입니다. 오류나 제안사항이 있으면 언제든지 개발자에게 말해주세요!
                """
            }
        }
    },
}