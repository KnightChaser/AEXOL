supported_commands = {
    "change_status"   : {
        "description" : "봇의 상태를 바꿉니다",
        "usage"       : "axl! change_status [online|offline|idle|do_not_disturb|invisible]",
        "privilege"   : "administrator"
    },
    "time"            : {
        "description" : "현재 시간을 초 단위로 알려줍니다. 단, 시간은 서버가 위치한 한국시(한국표준시, KST)를 기준으로 합니다.",
        "usage"       : "axl! time",
        "privilege"   : "everyone"
    },
    "hello"           : {
        "description" : "봇에게 인사를 시킵니다.",
        "usage"       : "axl! hello",
        "privilege"   : "everyone"
    },
    "help"            : {
        "description" : "도움말을 출력합니다.",
        "usage"       : "axl! help [command(without \"!\")]",
        "privilege"   : "everyone"
    },
    "ping"            : {
        "description" : "원하는 타겟의 네트워크 연결 상태를 확인합니다. (ICMP ECHO/REPLY)",
        "usage"       : "axl! ping [target_ip_address|target_url]",
        "privilege"   : "everone"
    },
    "voice_channel"   : {
        "description" : "봇을 음성 채널에 초대시키거나 나가도록 합니다. 이때, 초대하기 전 먼저 원하는 음성 채널에 사용자가 위치해야 합니다. 나갈 때는 음성 채널에 꼭 있지 않아도 됩니다.",
        "usage"       : "axl! voice_channel [join|leave]",
        "privilege"   : "everone",
        "detailed_descriptions" : {
            0 : {
                "title"     : "test_title_1",
                "content"   : "test_content_1"
            },
            1 : {
                "title"     : "test_title_2",
                "content"   : "test_content_2"
            }
        }
    },
}